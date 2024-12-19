from aiogram import Router, types
from database.models import Session, User
from utils.keyboards import generate_main_keyboard
from utils.translations import get_translation
import logging

logging.basicConfig(level=logging.INFO)

router = Router()

@router.message(lambda message: message.text in ["Русский", "English"])
async def set_language(message: types.Message):
    telegram_id = message.from_user.id
    selected_language = message.text

    session = Session()

    try:
        # Ищем пользователя
        user = session.query(User).filter_by(telegram_id=telegram_id).first()

        if user:
            user.language = selected_language
        else:
            user = User(
                telegram_id=telegram_id,
                language=selected_language,
                name="Unknown",  # Установим дефолтное имя, если его нет
                phone=None       # Допускаем пустой телефон
            )
            session.add(user)

        session.commit()

        # Отправляем сообщение с клавиатурой
        await message.answer(
            get_translation("menu_greeting", selected_language),
            reply_markup=generate_main_keyboard(selected_language)
        )

    except Exception as e:
        logging.error(f"Error saving language for user {telegram_id}: {e}")
        session.rollback()
        await message.answer("Произошла ошибка при сохранении языка. Попробуйте еще раз.")
    finally:
        session.close()
