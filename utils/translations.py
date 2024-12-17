translations = {
    "menu_greeting": {
        "English": "Welcome to the menu! Please select an option.",
        "Русский": "Добро пожаловать в меню! Выберите действие."
    },
    "choose_category": {
        "English": "Choose a category of bread:",
        "Русский": "Выберите категорию хлеба:"
    },
    "rye_bread": {
        "English": "Rye Bread",
        "Русский": "Ржаной хлеб"
    },
    "white_bread": {
        "English": "White Bread",
        "Русский": "Белый хлеб"
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
        "Русский": "Ваша корзина пуста.",
        "English": "Your cart is empty."
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
    "added_to_cart": {
        "Русский": "Товар добавлен в корзину!",
        "English": "Item added to cart!"
    },
    "error_adding_to_cart": {
        "Русский": "Ошибка при добавлении товара в корзину.",
        "English": "Error adding item to cart."
    },
    "language_prompt": {
        "Русский": "Пожалуйста, выберите язык:",
        "English": "Please select your language:"
    },
    "language_set": {
        "Русский": "Язык установлен: Русский.",
        "English": "Language set to English."
    },
    "language_changed": {
        "Русский": "Язык изменён на Русский.",
        "English": "Language changed to English."
    },
    "language_already_set": {
        "Русский": "Язык уже установлен на Русский.",
        "English": "The language is already set to English."
    },
    "welcome_back": {
        "Русский": "Добро пожаловать обратно!",
        "English": "Welcome back!"
    },
    "welcome_select_language": {
        "Русский": "Добро пожаловать! Пожалуйста, выберите язык:",
        "English": "Welcome! Please select your language:"
    },
    "details_button": {  # Кнопка для показа подробностей
        "Русский": "Подробнее",
        "English": "Details"
    },
    "collapse_button": {  # Кнопка для сворачивания подробностей
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
    "checkout_prompt": {
        "Русский": "Введите ваше имя, телефон и прикрепите скриншот оплаты.",
        "English": "Enter your name, phone number, and attach a payment receipt."
    },
    "back_to_cart": {
        "Русский": "Назад",
        "English": "Back"
    },
    "done_button": {
        "Русский": "Готово",
        "English": "Done"
    },
    "order_confirmed": {
        "Русский": "Ваш заказ принят! Оператор свяжется с вами в ближайшее время.",
        "English": "Your order has been received! Our operator will contact you shortly."
    }
}

def get_translation(key, language):
    """Получает перевод по ключу и языку."""
    return translations.get(key, {}).get(language, key)
