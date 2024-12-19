import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN

from handlers import start, menu, language,catalog,order,cart # Убедитесь, что все обработчики подключены

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Подключение маршрутов
dp.include_router(start.router)
dp.include_router(menu.router)
dp.include_router(language.router)
dp.include_router(catalog.router)
dp.include_router(cart.router)
dp.include_router(order.router)

# dp.include_router(location.router)


async def main():
    print("Бот запущен!")
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


