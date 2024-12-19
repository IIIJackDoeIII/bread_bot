import logging

translations = {
    "menu_greeting": {
        "English": "Welcome to the menu! Please select an option.",
        "Русский": "Добро пожаловать в меню! Выберите действие."
    },
    "choose_category": {
        "English": "Choose a category of bread:",
        "Русский": "Выберите категорию хлеба:"
    },
    "browse_bread": {
        "Русский": "Список хлеба",
        "English": "Browse Bread"
    },
    "my_order": {
        "Русский": "Мой заказ",
        "English": "My Order"
    },
    "change_language": {
        "Русский": "Сменить язык",
        "English": "Change Language"
    },
    "cart_empty": {
        "Русский": "❌ Ваша корзина пуста.",
        "English": "❌ Your cart is empty."
    },
    "cart_summary": {
        "Русский": "Содержимое корзины:",
        "English": "Cart contents:"
    },
    "cart_cleared": {
        "Русский": "Корзина очищена.",
        "English": "Cart cleared."
    },
    "add_to_cart_button": {
        "Русский": "Добавить к заказу",
        "English": "Add to Cart"
    },
    "checkout_button": {
        "Русский": "Оформить заказ",
        "English": "Proceed to Checkout"
    },
    "clear_cart_button": {
        "Русский": "Очистить корзину",
        "English": "Clear Cart"
    },
    "done_button": {
        "Русский": "Готово",
        "English": "Done"
    },
    "dynamic_form": {
        "Русский": "🔽 Форма заказа:",
        "English": "🔽 Order Form:"
    },
    "enter_name": {
        "Русский": "👉 Введите ваше имя:",
        "English": "👉 Enter your name:"
    },
    "enter_phone": {
        "Русский": "👉 Введите ваш телефон (например: +79123456789):",
        "English": "👉 Enter your phone number (e.g., +123456789):"
    },
    "attach_receipt": {
        "Русский": "👉 Прикрепите чек об оплате:",
        "English": "👉 Attach the payment receipt:"
    },
    "name_error": {
        "Русский": "❌ Имя должно содержать только буквы и быть длиннее одного символа.",
        "English": "❌ Name must contain only letters and be longer than one character."
    },
    "phone_error": {
        "Русский": "❌ Некорректный номер телефона. Попробуйте ещё раз.",
        "English": "❌ Invalid phone number. Please try again."
    },
    "name_saved": {
        "Русский": "✅ Имя сохранено!",
        "English": "✅ Name saved!"
    },
    "phone_saved": {
        "Русский": "✅ Телефон сохранён!",
        "English": "✅ Phone number saved!"
    },
    "receipt_uploaded": {
        "Русский": "✅ Чек успешно загружен!",
        "English": "✅ Receipt successfully uploaded!"
    },
    "not_specified": {
        "Русский": "Не указано",
        "English": "Not specified"
    },
    "order_summary": {
        "Русский": "📝 **Ваш заказ:**\n",
        "English": "📝 **Your Order:**\n"
    },
    "edit_order": {
        "Русский": "Исправить данные",
        "English": "Edit Details"
    },
    "confirm_order": {
        "Русский": "Оформить",
        "English": "Confirm Order"
    },
    "order_confirmed": {
        "Русский": "🎉 Ваш заказ оформлен! Администратор свяжется с вами в ближайшее время.",
        "English": "🎉 Your order has been placed! An administrator will contact you shortly."
    },
    "back_to_cart": {
        "Русский": "Назад",
        "English": "Back"
    },
    "back_prompt": {
        "Русский": "Для возврата нажмите 'Назад'.",
        "English": "Press 'Back' to return."
    },
    "uploaded": {
        "Русский": "Загружен",
        "English": "Uploaded"
    },
    "not_uploaded": {
        "Русский": "Не загружен",
        "English": "Not uploaded"
    },
    "return_to_cart": {
        "Русский": "Возвращаемся в корзину...",
        "English": "Returning to the cart..."
    },
    "begin_checkout": {
        "Русский": "Оформить",
        "English": "Begin Checkout"
    },
    "proceed_to_checkout": {
        "Русский": "Оформить заказ",
        "English": "Proceed to Checkout"
    },
    "details_button": {
        "Русский": "Подробнее",
        "English": "Details"
    },
    "collapse_button": {
        "Русский": "Свернуть",
        "English": "Collapse"
    },
    "info_unavailable": {
        "Русский": "Информация недоступна.",
        "English": "Information unavailable."
    },
    "full_description": {
        "Русский": "Полное описание: Это пример полного описания.",
        "English": "Full description: This is a sample full description."
    },
    "order_summary_name": {
    "Русский": "Имя: ",
    "English": "Name: "
},
"order_summary_phone": {
    "Русский": "Телефон: ",
    "English": "Phone: "
},
"order_summary_receipt": {
    "Русский": "Чек: ",
    "English": "Receipt: "
},
"receipt_attached": {
    "Русский": "Прикреплен",
    "English": "Attached"
},
"receipt_not_attached": {
    "Русский": "Не прикреплен",
    "English": "Not attached"
},
"order_details": {
    "Русский": "Информация о заказе",
    "English": "Order Details"
},
}

def get_translation(key, language):
    """Получает перевод по ключу и языку."""
    translation = translations.get(key, {}).get(language, key)
    if translation == key:
        logging.warning(f"Перевод для ключа '{key}' и языка '{language}' отсутствует. Используется ключ по умолчанию.")
    return translation

