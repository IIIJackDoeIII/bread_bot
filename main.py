import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from keep_alive import keep_alive

from handlers import start, menu, language, catalog, order, cart  # Убедитесь, что все обработчики подключены

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация всех обработчиков (если есть соответствующий метод в модуле handlers)
dp.include_router(start.router)
dp.include_router(menu.router)
dp.include_router(language.router)
dp.include_router(catalog.router)
dp.include_router(order.router)
dp.include_router(cart.router)

if __name__ == "__main__":
    keep_alive()  # Запуск HTTP-сервера
    # Асинхронный запуск поллинга
    asyncio.run(dp.start_polling(bot))
