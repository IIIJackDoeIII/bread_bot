from aiogram import Router, types
from aiogram.types import FSInputFile
from database.models import Session, User
from utils.translations import get_translation
from utils.keyboards import generate_main_keyboard

import logging
from bread_data import BREADS  # Подключаем данные о хлебе

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Функция для получения языка пользователя из базы данных
def get_user_language_from_db(telegram_id):
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            logger.info(f"User {telegram_id} language: {user.language}")
            return user.language
        else:
            logger.warning(f"User {telegram_id} not found. Defaulting to Русский.")
            return "Русский"
    finally:
        session.close()

# Обработчик кнопки "Список хлеба"
@router.message(lambda message: message.text in ["Browse Bread", "Список хлеба"])
async def browse_bread(message: types.Message):
    telegram_id = message.from_user.id

    # Получаем язык пользователя
    language = get_user_language_from_db(telegram_id)
    logger.info(f"User {telegram_id} selected language: {language}")

    # Проверяем, есть ли данные о хлебе
    if not BREADS:
        logger.error("BREADS data is empty or not loaded.")
        await message.answer(
            get_translation("no_bread_available", language),
            reply_markup=generate_main_keyboard(language)  # Показываем клавиатуру главного меню
        )
        return

    # Формируем список категорий хлеба
    bread_buttons = [
        types.InlineKeyboardButton(
            text=bread["name"][language], callback_data=f"view_bread:{bread_type}"
        )
        for bread_type, bread in BREADS.items()
    ]
    bread_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[bread_buttons])

    # Отправляем список категорий хлеба
    await message.answer(
        get_translation("choose_category", language),
        reply_markup=bread_keyboard
    )

    # После вывода категорий хлеба переключаем клавиатуру на главное меню
    await message.answer(
        get_translation("menu_greeting", language),
        reply_markup=generate_main_keyboard(language)  # Главное меню
    )

# Обработчик для показа подкатегорий хлеба
@router.callback_query(lambda callback_query: callback_query.data.startswith("view_bread:"))
async def view_bread_list(callback_query: types.CallbackQuery):
    telegram_id = callback_query.from_user.id
    bread_type = callback_query.data.split(":")[1]

    # Получаем язык пользователя
    language = get_user_language_from_db(telegram_id)
    logger.info(f"User {telegram_id} selected language: {language}")

    bread = BREADS.get(bread_type)
    if bread and "subcategories" in bread:
        for sub_id, sub in bread["subcategories"].items():
            try:
                photo_file = FSInputFile(sub["image"])  # Локальный файл
                await callback_query.message.answer_photo(
                    photo=photo_file,
                    caption=f"<b>{sub['name'][language]}</b>\n\n{sub['short_description'][language]}",
                    reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text=get_translation("details_button", language),
                                    callback_data=f"expand_bread:{bread_type}:{sub_id}"
                                ),
                                types.InlineKeyboardButton(
                                    text=get_translation("add_to_cart_button", language),
                                    callback_data=f"add_to_cart:{bread_type}:{sub_id}"
                                )
                            ]
                        ]
                    ),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Error sending bread image: {e}")
    else:
        logger.warning(f"Bread category {bread_type} not found for user {telegram_id}.")
        await callback_query.message.answer(
            get_translation("category_not_found", language)
        )
    await callback_query.answer()


# Обработчик для показа подробной информации
@router.callback_query(lambda callback_query: callback_query.data.startswith("expand_bread:"))
async def expand_bread_details(callback_query: types.CallbackQuery):
    _, bread_type, sub_id = callback_query.data.split(":")
    telegram_id = callback_query.from_user.id

    language = get_user_language_from_db(telegram_id)
    logger.info(f"User {telegram_id} requested details for {bread_type}:{sub_id}")

    bread = BREADS.get(bread_type)
    sub = bread["subcategories"].get(sub_id) if bread else None

    if sub:
        await callback_query.message.edit_caption(
            caption=f"<b>{sub['name'][language]}</b>\n\n{sub['full_description'][language]}\n\n",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text=get_translation("collapse_button", language),
                            callback_data=f"collapse_bread:{bread_type}:{sub_id}"
                        ),
                        types.InlineKeyboardButton(
                            text=get_translation("add_to_cart_button", language),
                            callback_data=f"add_to_cart:{bread_type}:{sub_id}"
                        )
                    ]
                ]
            ),
            parse_mode="HTML"
        )
    else:
        logger.error(f"Bread subcategory {sub_id} not found.")
        await callback_query.answer(get_translation("info_unavailable", language), show_alert=True)

# Обработчик для сворачивания подробной информации
@router.callback_query(lambda callback_query: callback_query.data.startswith("collapse_bread:"))
async def collapse_bread_details(callback_query: types.CallbackQuery):
    _, bread_type, sub_id = callback_query.data.split(":")
    telegram_id = callback_query.from_user.id

    language = get_user_language_from_db(telegram_id)
    logger.info(f"User {telegram_id} requested to collapse details for {bread_type}:{sub_id}")

    bread = BREADS.get(bread_type)
    sub = bread["subcategories"].get(sub_id) if bread else None

    if sub:
        await callback_query.message.edit_caption(
            caption=f"<b>{sub['name'][language]}</b>\n\n{sub['short_description'][language]}",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text=get_translation("details_button", language),
                            callback_data=f"expand_bread:{bread_type}:{sub_id}"
                        ),
                        types.InlineKeyboardButton(
                            text=get_translation("add_to_cart_button", language),
                            callback_data=f"add_to_cart:{bread_type}:{sub_id}"
                        )
                    ]
                ]
            ),
            parse_mode="HTML"
        )
    else:
        logger.error(f"Bread subcategory {sub_id} not found.")
        await callback_query.answer(get_translation("info_unavailable", language), show_alert=True)
