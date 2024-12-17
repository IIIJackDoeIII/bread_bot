from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils.translations import get_translation


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils.translations import get_translation

def generate_main_keyboard(language: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("browse_bread", language))],
            [
                KeyboardButton(text=get_translation("my_order", language)),
                KeyboardButton(text=get_translation("change_language", language)),
            ],
        ],
        resize_keyboard=True
    )

def generate_cart_keyboard(language: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("browse_bread", language))],
            [
                KeyboardButton(text=get_translation("checkout_button", language)),
                KeyboardButton(text=get_translation("clear_cart_button", language)),
            ],
        ],
        resize_keyboard=True
    )


def language_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="English")],
            [KeyboardButton(text="Русский")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )



