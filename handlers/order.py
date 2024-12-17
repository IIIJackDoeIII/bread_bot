from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import Session, User, CartItem, Order
from utils.translations import get_translation
from utils.keyboards import generate_main_keyboard, generate_cart_keyboard
from config import ADMINS
import json
import logging
import re

router = Router()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния FSM для оформления заказа
class CheckoutForm(StatesGroup):
    waiting_for_data = State()

# Генерация инлайн-клавиатуры для заполнения данных
def generate_checkout_form_keyboard(name_filled, phone_filled, receipt_uploaded):
    buttons = [
        [types.InlineKeyboardButton(text="✅ Имя" if name_filled else "Имя", callback_data="input_name")],
        [types.InlineKeyboardButton(text="✅ Телефон" if phone_filled else "Телефон", callback_data="input_phone")],
        [types.InlineKeyboardButton(text="✅ Чек" if receipt_uploaded else "Прикрепить чек", callback_data="upload_receipt")],
        [
            types.InlineKeyboardButton(
                text="Готово" if name_filled and phone_filled and receipt_uploaded else "Готово (недоступно)",
                callback_data="submit_order" if name_filled and phone_filled and receipt_uploaded else "disabled",
            )
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


# 1. Обработчик для отображения корзины
@router.message(lambda message: message.text in ["Мой заказ", "My Order"])
async def view_cart(message: types.Message):
    telegram_id = message.from_user.id
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await message.answer(get_translation("cart_empty", "Русский"), reply_markup=generate_main_keyboard("Русский"))
            return

        language = user.language
        cart_items = session.query(CartItem).filter_by(user_id=user.id).all()

        if not cart_items:
            await message.answer(get_translation("cart_empty", language), reply_markup=generate_main_keyboard(language))
        else:
            cart_details = "\n".join([f"{item.bread_type}: {item.quantity}" for item in cart_items])
            await message.answer(
                f"{get_translation('cart_summary', language)}\n{cart_details}",
                reply_markup=generate_cart_keyboard(language)
            )
    finally:
        session.close()

# 2. Очистка корзины
@router.message(lambda message: message.text in ["Очистить корзину", "Clear Cart"])
async def clear_cart_command(message: types.Message):
    telegram_id = message.from_user.id
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        language = user.language if user else "Русский"

        if user:
            session.query(CartItem).filter_by(user_id=user.id).delete()
            session.commit()
            await message.answer(get_translation("cart_cleared", language), reply_markup=generate_main_keyboard(language))
        else:
            await message.answer(get_translation("cart_empty", language))
    finally:
        session.close()

# 3. Лог добавления товара в корзину
@router.callback_query(lambda callback_query: callback_query.data.startswith("add_to_cart:"))
async def add_to_cart_handler(callback_query: types.CallbackQuery):
    telegram_id = callback_query.from_user.id
    data_parts = callback_query.data.split(":")
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id, language="Русский")
            session.add(user)
            session.commit()

        bread_type = data_parts[1]
        cart_item = session.query(CartItem).filter_by(user_id=user.id, bread_type=bread_type).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            session.add(CartItem(user_id=user.id, bread_type=bread_type, quantity=1))
        session.commit()

        await callback_query.answer(get_translation("added_to_cart", user.language), show_alert=True)
    finally:
        session.close()

# 4. Обработчик для оформления заказа
@router.message(lambda message: message.text in ["Оформить заказ", "Proceed to Checkout"])
async def proceed_to_checkout(message: types.Message, state: FSMContext):
    await state.set_state(CheckoutForm.waiting_for_data)
    await state.update_data(name=None, phone=None, receipt=None)
    keyboard = generate_checkout_form_keyboard(False, False, False)
    await message.answer("Заполните форму для оформления заказа:", reply_markup=keyboard)

# Обработчики ввода данных
@router.callback_query(F.data == "input_name")
async def input_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ваше имя:")
    await state.update_data(current_field="name")

@router.callback_query(F.data == "input_phone")
async def input_phone(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ваш телефон (например: +79123456789):")
    await state.update_data(current_field="phone")

@router.callback_query(F.data == "upload_receipt")
async def upload_receipt(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Пожалуйста, прикрепите скриншот оплаты:")
    await state.update_data(current_field="receipt")

# Обработчик текстового ввода и файла
@router.message()
async def handle_input(message: types.Message, state: FSMContext):
    """Обработчик для ввода данных формы"""
    data = await state.get_data()
    current_field = data.get("current_field")

    # Логируем тип сообщения для диагностики
    logger.info(f"Получено сообщение: {message.content_type}")

    # Обработка имени
    if current_field == "name":
        await state.update_data(name=message.text)
        await message.answer("Имя сохранено!")

    # Обработка телефона
    elif current_field == "phone":
        if not message.text.startswith("+") or not message.text[1:].isdigit():
            await message.answer("Некорректный номер телефона. Попробуйте ещё раз.")
            return
        await state.update_data(phone=message.text)
        await message.answer("Телефон сохранен!")

    # Обработка прикреплённого изображения (чека)
    elif current_field == "receipt" and message.photo:
        file_id = message.photo[-1].file_id  # Самое большое изображение
        logger.info(f"Чек загружен как изображение: file_id = {file_id}")
        await state.update_data(receipt=file_id)
        await message.answer("Чек успешно прикреплён!")

    # Обновляем форму с кнопками
    user_data = await state.get_data()
    keyboard = generate_checkout_form_keyboard(
        user_data.get("name") is not None,
        user_data.get("phone") is not None,
        user_data.get("receipt") is not None,
    )
    await message.answer("Обновлённая форма:", reply_markup=keyboard)
    


# Обработчик "Готово"
@router.callback_query(F.data == "submit_order")
async def submit_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    telegram_id = callback.from_user.id
    session = Session()

    try:
        # Получение данных о пользователе и заказе
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        cart_items = session.query(CartItem).filter_by(user_id=user.id).all()

        if not cart_items:
            await callback.message.answer("Ваша корзина пуста. Добавьте товары перед оформлением заказа.")
            return

        order_details = [{"bread_type": item.bread_type, "quantity": item.quantity} for item in cart_items]

        # Создание заказа
        new_order = Order(
            user_id=user.id,
            name=data['name'],
            phone=data['phone'],
            details=json.dumps(order_details),
            receipt=data.get("receipt"),
        )
        session.add(new_order)
        session.query(CartItem).filter_by(user_id=user.id).delete()
        session.commit()

        # Логирование данных перед экранированием
        logger.info(f"RAW DATA: name={data['name']}, phone={data['phone']}, telegram_id={user.telegram_id}")
        logger.info(f"RAW ORDER DETAILS: {order_details}")
        logger.info(f"RAW RECEIPT: {data.get('receipt')}")

        # Формирование данных заказа
        order_summary = "\n".join([f" {escape_markdown_v2(item['bread_type'])}: {item['quantity']}" for item in order_details])
        telegram_link = f'<a href="tg://user?id={user.telegram_id}">Перейти к чату</a>'

        log_message = (
            f"<b>Новый заказ</b>\n"
            f"👤 <b>Имя:</b> {data['name']}<br>"
            f"📞 <b>Телефон:</b> {data['phone']}<br>"
            f"🆔 <b>Telegram:</b> {telegram_link}<br><br>"
            f"🛒 <b>Детали заказа:</b><br>{order_summary}"
        )

        logger.info(f"Generated Telegram Link: {telegram_link}")
        logger.info(f"Generated Log Message:\n{log_message}")

        # Уведомление администраторов
        for admin_chat_id in ADMINS:
            # Отправка основного сообщения
            await callback.message.bot.send_message(
                chat_id=admin_chat_id,
                text=log_message,
                parse_mode="MarkdownV2"
            )

            # Если чек (скриншот) загружен, отправляем как фото
            receipt_file_id = data.get("receipt")
            if receipt_file_id:
                await callback.message.bot.send_photo(
                    chat_id=admin_chat_id,
                    photo=receipt_file_id,
                    caption="📎 Чек об оплате"
                )

        # Подтверждение пользователю
        await callback.message.answer("Ваш заказ успешно оформлен!", reply_markup=generate_main_keyboard(user.language))
        await state.clear()

    except Exception as e:
        logger.error(f"Ошибка при оформлении заказа: {e}")
        await callback.message.answer("Произошла ошибка при оформлении заказа. Попробуйте ещё раз.")

    finally:
        session.close()



def escape_markdown_v2(text: str) -> str:
    """
    Экранирует специальные символы для Telegram MarkdownV2.
    :param text: Исходный текст, который нужно экранировать.
    :return: Текст с экранированными символами.
    """
    if not text:
        return ""
    # Добавляем экранирование символа "!" и других
    escape_chars = r"([_*\[\]()~`>#+\-=|{}.!\\<>])"
    return re.sub(escape_chars, r"\\\1", text)






@router.callback_query(F.data == "disabled")
async def disabled_button(callback: types.CallbackQuery):
    await callback.answer("Пожалуйста, заполните все поля формы.", show_alert=True)