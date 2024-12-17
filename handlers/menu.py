from aiogram import types, Router
from database.models import Session, User
from utils.keyboards import generate_main_keyboard

router = Router()

# Обработчик кнопки "Список хлеба"
@router.message(lambda message: message.text in ["Browse Bread 🍞", "Список хлеба 🍞"])
async def browse_bread(message: types.Message):
    session = Session()
    telegram_id = message.from_user.id

    # Получаем язык пользователя
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    language = user.language if user else "Русский"

    # Отображаем категории хлеба
    await message.answer(
        "Choose a category of bread:" if language == "English" else "Выберите категорию хлеба:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton("Rye Bread" if language == "English" else "Ржаной хлеб")],
                [types.KeyboardButton("White Bread" if language == "English" else "Белый хлеб")],
                [types.KeyboardButton("Back to Menu" if language == "English" else "Назад в меню")]
            ],
            resize_keyboard=True
        )
    )
    session.close()
