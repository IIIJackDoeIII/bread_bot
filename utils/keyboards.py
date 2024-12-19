from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils.translations import get_translation
from aiogram import types



# Основное меню
def generate_main_keyboard(language: str):
    """Генерация основной клавиатуры."""
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

# Клавиатура для шага "Назад" при работе с формой
def generate_back_only_keyboard(language: str):
    """
    Генерация клавиатуры с одной кнопкой "Назад" на выбранном языке.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("back_to_cart", language))],
        ],
        resize_keyboard=True
    )


# Клавиатура для корзины
def generate_cart_keyboard(language: str):
    """Генерация клавиатуры для раздела корзины."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("browse_bread", language))],  # Список товаров
            [
                KeyboardButton(text=get_translation("checkout_button", language)),  # Оформить заказ
                KeyboardButton(text=get_translation("clear_cart_button", language))  # Очистить корзину
            ],
        ],
        resize_keyboard=True
    )





# Клавиатура выбора языка
def language_keyboard():
    """Генерация клавиатуры для выбора языка."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="English")],
            [KeyboardButton(text="Русский")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.translations import get_translation

def generate_checkout_form_keyboard(name_filled, phone_filled, receipt_uploaded, language):
    buttons = [
        [
            types.InlineKeyboardButton(
                text=get_translation("enter_name", language) if not name_filled else get_translation("name_saved", language),
                callback_data="input_name"
            )
        ],
        [
            types.InlineKeyboardButton(
                text=get_translation("enter_phone", language) if not phone_filled else get_translation("phone_saved", language),
                callback_data="input_phone"
            )
        ],
        [
            types.InlineKeyboardButton(
                text=get_translation("attach_receipt", language) if not receipt_uploaded else get_translation("receipt_uploaded", language),
                callback_data="input_receipt"
            )
        ]
    ]

    # Добавляем кнопку "Done" только если все поля заполнены
    if name_filled and phone_filled and receipt_uploaded:
        buttons.append([
            types.InlineKeyboardButton(
                text=get_translation("done_button", language),
                callback_data="submit_order"
            )
        ])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_cart_keyboard_with_quantity(cart_items, language):
    """
    Генерация клавиатуры корзины с кнопками увеличения и уменьшения количества товаров.
    """
    buttons = []
    for item in cart_items:
        buttons.append([
            InlineKeyboardButton(
                text="➖",
                callback_data=f"decrease_{item.id}"
            ) if item.quantity > 1 else InlineKeyboardButton(
                text="➖",
                callback_data="noop"
            ),
            InlineKeyboardButton(
                text=f"{item.bread_type}: {item.quantity}",
                callback_data="noop"
            ),
            InlineKeyboardButton(
                text="➕",
                callback_data=f"increase_{item.id}"
            )
        ])
    
    # Добавляем кнопки "Оформить заказ" и "Очистить корзину"
    buttons.append([
        InlineKeyboardButton(
            text=get_translation("checkout_button", language),
            callback_data="proceed_to_checkout"
        ),
        InlineKeyboardButton(
            text=get_translation("clear_cart_button", language),
            callback_data="clear_cart"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


