from aiogram import types, Router
from aiogram.filters import Command
from database.models import Session, User, CartItem
from utils.keyboards import language_keyboard, generate_main_keyboard
from utils.translations import get_translation

import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Обработчик команды /start
@router.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    """Обработчик команды /start."""
    session = Session()
    telegram_id = message.from_user.id

    try:
        # Проверяем, есть ли пользователь в базе данных
        user = session.query(User).filter_by(telegram_id=telegram_id).first()

        if user:
            # Пользователь уже существует — используем его язык
            logger.info(f"Existing user {telegram_id} with language {user.language}")
            await message.answer(
                get_translation("welcome_back", user.language),
                reply_markup=generate_main_keyboard(user.language)
            )
        else:
            # Новый пользователь — предлагаем выбрать язык (двуязычное сообщение)
            logger.info(f"New user {telegram_id} started the bot.")
            await message.answer(
                "Welcome! / Добро пожаловать!\nPlease select your language / Пожалуйста, выберите язык:",
                reply_markup=language_keyboard()
            )
    finally:
        session.close()


# Обработчик кнопки "Сменить язык"
@router.message(lambda message: message.text in ["Сменить язык", "Change Language"])
async def change_language(message: types.Message):
    """Обработчик для кнопки 'Сменить язык'"""
    logger.info(f"User {message.from_user.id} wants to change language.")
    await message.answer(
        get_translation("language_prompt", "Русский"),
        reply_markup=language_keyboard()
    )


# Обработчик выбора языка из клавиатуры
@router.message(lambda message: message.text in ["Русский", "English"])
async def set_language(message: types.Message):
    """Обработчик выбора и смены языка пользователя."""
    session = Session()
    telegram_id = message.from_user.id

    try:
        # Получаем пользователя из базы данных
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        selected_language = message.text

        # Логика для нового пользователя
        if not user:
            user = User(telegram_id=telegram_id, language=selected_language)
            session.add(user)
            session.commit()
            logger.info(f"New user created: {telegram_id} with language {selected_language}")
            await message.answer(
                get_translation("language_set", selected_language),
                reply_markup=generate_main_keyboard(selected_language)
            )
            return

        # Логика для существующего пользователя
        if user.language == selected_language:
            logger.info(f"User {telegram_id} selected the same language: {selected_language}")
            await message.answer(
                get_translation("language_already_set", selected_language)
            )
        else:
            # Обновляем язык пользователя
            user.language = selected_language
            session.commit()
            logger.info(f"User {telegram_id} changed language to {selected_language}")

            # Проверяем наличие товаров в корзине
            cart_items = session.query(CartItem).filter_by(user_id=user.id).count()
            if cart_items > 0:
                await message.answer(
                    f"{get_translation('language_changed', selected_language)} {get_translation('cart_summary', selected_language)}",
                    reply_markup=generate_main_keyboard(selected_language)
                )
            else:
                await message.answer(
                    get_translation("language_changed", selected_language),
                    reply_markup=generate_main_keyboard(selected_language)
                )
    finally:
        session.close()
