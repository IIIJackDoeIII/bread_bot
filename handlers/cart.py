from aiogram import Router, types
from database.models import Session, User, CartItem
from utils.translations import get_translation
from utils.keyboards import generate_main_keyboard, generate_cart_keyboard
import logging

router = Router()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==== Базовые функции ====

def get_or_create_user(telegram_id: int) -> User:
    """
    Получает пользователя из БД или создает нового.
    """
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, language="Русский")
        session.add(user)
        session.commit()
    return user


def get_cart_details(user_id: int) -> str:
    """
    Получает содержимое корзины пользователя.
    """
    session = Session()
    cart_items = session.query(CartItem).filter_by(user_id=user_id).all()
    if not cart_items:
        return ""
    return "\n".join([f"{item.bread_type}: {item.quantity}" for item in cart_items])


def clear_cart(user_id: int):
    """
    Очищает корзину пользователя.
    """
    session = Session()
    session.query(CartItem).filter_by(user_id=user_id).delete()
    session.commit()
    session.close()


# ==== Обработчики ====

# 1. Просмотр корзины
@router.message(lambda message: message.text in ["Мой заказ", "My Order"])
async def view_cart(message: types.Message):
    telegram_id = message.from_user.id
    user = get_or_create_user(telegram_id)
    language = user.language

    cart_details = get_cart_details(user.id)
    
    if not cart_details:
        await message.answer(get_translation("cart_empty", language), reply_markup=generate_main_keyboard(language))
    else:
        await message.answer(
            f"{get_translation('cart_summary', language)}\n{cart_details}",
            reply_markup=generate_cart_keyboard(language)
        )


# 2. Очистка корзины
@router.message(lambda message: message.text in ["Очистить корзину", "Clear Cart"])
async def clear_cart_command(message: types.Message):
    telegram_id = message.from_user.id
    user = get_or_create_user(telegram_id)
    language = user.language

    clear_cart(user.id)
    await message.answer(get_translation("cart_cleared", language), reply_markup=generate_main_keyboard(language))


# 3. Добавление товара в корзину
@router.callback_query(lambda callback_query: callback_query.data.startswith("add_to_cart:"))
async def add_to_cart_handler(callback_query: types.CallbackQuery):
    bread_type = callback_query.data.split(":")[1]
    telegram_id = callback_query.from_user.id
    session = Session()
    try:
        user = get_or_create_user(telegram_id)

        # Добавляем товар или увеличиваем количество
        cart_item = session.query(CartItem).filter_by(user_id=user.id, bread_type=bread_type).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            session.add(CartItem(user_id=user.id, bread_type=bread_type, quantity=1))

        session.commit()
        await callback_query.answer(get_translation("added_to_cart", user.language), show_alert=True)

    except Exception as e:
        logger.error(f"Ошибка при добавлении товара: {e}")
        await callback_query.answer(get_translation("error_adding_to_cart", user.language), show_alert=True)
    finally:
        session.close()
