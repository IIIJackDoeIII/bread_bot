from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import Session, User
from utils.keyboards import (
    generate_checkout_form_keyboard,
    generate_back_only_keyboard
)
from utils.translations import get_translation

from config import ADMINS  # Импортируем список администраторов из конфигаfrom utils.translations import get_translation


from database.models import CartItem, Order
import logging

router = Router()
logging.basicConfig(level=logging.INFO)

# Состояния FSM для формы заказа
class CheckoutForm(StatesGroup):
    waiting_for_data = State()


# Динамическая форма
async def send_dynamic_form(message: types.Message, state: FSMContext, language: str):
    data = await state.get_data()
    logging.info(f"Form data: {data}")
    logging.info(f"Language: {language}")
    current_field = data.get("current_field", None)
    name_filled = bool(data.get("name"))
    phone_filled = bool(data.get("phone"))
    receipt_uploaded = bool(data.get("receipt"))

    # Отправка формы с локализацией
    await message.answer(
        get_translation("dynamic_form", language),
        reply_markup=generate_checkout_form_keyboard(
            name_filled=name_filled,
            phone_filled=phone_filled,
            receipt_uploaded=receipt_uploaded,
            language=language  # Используем переданный язык
        )
    )

    # Логика отправки запроса данных
    if current_field == "name":
        await message.answer(get_translation("enter_name", language))
    elif current_field == "phone":
        await message.answer(get_translation("enter_phone", language))
    elif current_field == "receipt":
        await message.answer(get_translation("attach_receipt", language))
    elif not current_field:
        if not name_filled:
            await message.answer(get_translation("enter_name", language))
            await state.update_data(current_field="name")
        elif not phone_filled:
            await message.answer(get_translation("enter_phone", language))
            await state.update_data(current_field="phone")
        elif not receipt_uploaded:
            await message.answer(get_translation("attach_receipt", language))
            await state.update_data(current_field="receipt")


  


# Обработчик "Оформить заказ"
# Обработчик "Оформить заказ"
@router.message(F.text.in_([
    get_translation("proceed_to_checkout", "Русский"),
    get_translation("proceed_to_checkout", "English")
]))
async def proceed_to_checkout(message: types.Message, state: FSMContext):
    """
    Вместо показа промежуточной клавиатуры сразу запускаем форму.
    """
    telegram_id = message.from_user.id
    session = Session()

    try:
        # Получаем язык пользователя из базы
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user_language = user.language if user and user.language else "Русский"

        # Сразу вызываем start_dynamic_form для перехода к форме
        await start_dynamic_form(message, state)

    finally:
        session.close()





# Обработчик кнопки "Оформить"
@router.message(F.text.in_([
    get_translation("begin_checkout", "Русский"),
    get_translation("begin_checkout", "English")
]))
async def start_dynamic_form(message: types.Message, state: FSMContext):
    """
    Показывает форму и заменяет клавиатуру на кнопку "Назад" с учётом локализации.
    """
    telegram_id = message.from_user.id

    # Получаем язык пользователя из базы
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user_language = user.language if user and user.language else "Русский"
    finally:
        session.close()

    # Устанавливаем состояние и данные из БД
    await state.set_state(CheckoutForm.waiting_for_data)
    await state.update_data(
        name=user.name if user and user.name else None,
        phone=user.phone if user and user.phone else None,
        receipt=None
    )

    # Отправка динамической формы на нужном языке
    await send_dynamic_form(message, state, user_language)

    # Заменяем клавиатуру на кнопку "Назад" с локализованным текстом
    await message.answer(
        get_translation("back_prompt", user_language),
        reply_markup=generate_back_only_keyboard(user_language)
    )



# Обработчик кнопки "Назад"
@router.message(F.text.in_([
    get_translation("back_to_cart", "Русский"),
    get_translation("back_to_cart", "English")
]))
async def back_to_cart(message: types.Message):
    from handlers.cart import view_cart
    telegram_id = message.from_user.id

    # Получаем язык пользователя из базы
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user_language = user.language if user and user.language else "Русский"
    finally:
        session.close()


    # Вызываем функцию отображения корзины
    await view_cart(message)


# Обработчик ввода данных
@router.message(CheckoutForm.waiting_for_data)
async def handle_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_field = data.get("current_field")

    session = Session()
    telegram_id = message.from_user.id

    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user_language = user.language if user and user.language else "Русский"

        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)

        if current_field == "name":
            if not message.text.isalpha() or len(message.text) < 2:
                await message.answer(get_translation("name_error", user_language))
                return
            user.name = message.text
            await state.update_data(name=message.text, current_field=None)
            await message.answer(get_translation("name_saved", user_language))

        elif current_field == "phone":
            if not message.text.startswith("+") or not message.text[1:].isdigit():
                await message.answer(get_translation("phone_error", user_language))
                return
            user.phone = message.text
            await state.update_data(phone=message.text, current_field=None)
            await message.answer(get_translation("phone_saved", user_language))

        elif current_field == "receipt" and message.photo:
            file_id = message.photo[-1].file_id
            user.receipt = file_id
            await state.update_data(receipt=file_id, current_field=None)
            await message.answer(get_translation("receipt_uploaded", user_language))

        session.commit()

    finally:
        session.close()

    await send_dynamic_form(message, state, user_language)




# Обработчик кнопки "Готово"
@router.callback_query(F.data == "submit_order")
async def finalize_form(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    session = Session()

    try:
        # Получаем данные из состояния FSM
        data = await state.get_data()
        name = data.get("name", "Не указано")
        phone = data.get("phone", "Не указано")
        receipt = data.get("receipt", None)

        # Получаем пользователя
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user_language = user.language if user and user.language else "Русский"

        # Получаем товары из корзины
        cart_items = session.query(CartItem).filter_by(user_id=user.id).all()
        if not cart_items:
            await callback.message.answer(get_translation("cart_empty", user_language))
            return

        # Формируем строку с деталями товаров
        order_details = "\n".join(
            [f"🍞 {item.bread_type}: {item.quantity} шт." for item in cart_items]
        )

        # Формируем итоговый чек
        order_summary = (
            f"{get_translation('order_summary_name', user_language)}{name}\n"
            f"{get_translation('order_summary_phone', user_language)}{phone}\n"
            f"{get_translation('order_summary_receipt', user_language)}"
            f"{get_translation('receipt_attached', user_language) if receipt else get_translation('receipt_not_attached', user_language)}\n\n"
            f"📦 {get_translation('order_details', user_language)}:\n{order_details}"
        )

        # Клавиатура для подтверждения или исправления данных
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=get_translation("edit_order", user_language), callback_data="edit_order")],
            [types.InlineKeyboardButton(text=get_translation("confirm_order", user_language), callback_data="confirm_order")]
        ])

        # Отправляем итоговый чек
        await callback.message.answer(order_summary, parse_mode="Markdown", reply_markup=keyboard)

    finally:
        session.close()


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    session = Session()

    try:
        # Получаем пользователя
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await callback.message.answer("❌ Пользователь не найден.")
            return

        # Получаем текущий язык пользователя
        user_language = user.language if user and user.language else "Русский"

        # Получаем данные из FSM
        data = await state.get_data()
        name = data.get("name", user.name or get_translation("not_specified", user_language))
        phone = data.get("phone", user.phone or get_translation("not_specified", user_language))
        receipt_file_id = data.get("receipt")

        # Проверяем корзину
        cart_items = session.query(CartItem).filter_by(user_id=user.id).all()
        if not cart_items:
            await callback.message.answer(get_translation("cart_empty", user_language))
            return

        # Формируем строку с деталями товаров
        order_details = "\n".join(
            [f"🍞 {item.bread_type}: {item.quantity} шт." for item in cart_items]
        )

        # Получаем данные пользователя из Telegram
        user_info = await callback.bot.get_chat(telegram_id)
        telegram_link = (
            f"[@{user_info.username}](https://t.me/{user_info.username})"
            if user_info.username
            else f"[Ссылка на профиль](tg://user?id={telegram_id})"
        )

        # Формируем сообщение для администратора
        admin_message = (
            f"🆕 {get_translation('order_admin_notification', user_language)}\n"
            f"👤 {get_translation('order_summary_name', user_language)}{name}\n"
            f"📞 {get_translation('order_summary_phone', user_language)}{phone}\n"
            f"📎 {get_translation('order_summary_receipt', user_language)}"
            f"{get_translation('receipt_attached', user_language) if receipt_file_id else get_translation('receipt_not_attached', user_language)}\n\n"
            f"📦 {get_translation('order_details', user_language)}:\n{order_details}\n"
            f"💬 Telegram: {telegram_link}"
        )

        # Сообщение пользователю
        await callback.message.answer(get_translation("order_confirmed", user_language))

        # Удаляем корзину и очищаем состояние FSM
        session.query(CartItem).filter_by(user_id=user.id).delete()
        session.commit()
        await state.clear()

        # Отправляем сообщение администраторам
        for admin_id in ADMINS:
            try:
                await callback.bot.send_message(admin_id, admin_message, parse_mode="Markdown")
                if receipt_file_id:
                    await callback.bot.send_photo(admin_id, photo=receipt_file_id, caption=get_translation("receipt_uploaded", user_language))
            except Exception as e:
                logging.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")

    finally:
        session.close()

    # Подтверждаем нажатие кнопки
    await callback.answer()




# Обработчик кнопки "Исправить данные"
@router.callback_query(F.data == "edit_order")
async def edit_order(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    session = Session()

    try:
        # Получаем данные пользователя
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user_language = user.language if user and user.language else "Русский"

        # Сохраняем язык в состоянии FSM
        logging.info(f"1 Язык пользователя в edit_order: {user_language}")
        await state.update_data(language=user_language, current_field=None)
        logging.info(f"2 Язык пользователя в edit_order: {user_language}")


        # Отправляем форму с текущими данными пользователя
        await send_dynamic_form(callback.message, state, user_language)

    finally:
        session.close()

    # Подтверждаем действие
    await callback.answer()







# Обработчик выбора поля для редактирования
@router.callback_query(F.data.startswith("input_"))
async def handle_field_edit(callback: types.CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    telegram_id = callback.from_user.id

    # Получаем язык пользователя из базы данных
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user_language = user.language if user and user.language else "Русский"
    finally:
        session.close()

    # Обновляем состояние
    await state.update_data(current_field=field)
    await callback.answer()

    # Отправляем локализованное сообщение в зависимости от поля
    if field == "name":
        await callback.message.answer(get_translation("enter_name", user_language))
    elif field == "phone":
        await callback.message.answer(get_translation("enter_phone", user_language))
    elif field == "receipt":
        await callback.message.answer(get_translation("attach_receipt", user_language))

