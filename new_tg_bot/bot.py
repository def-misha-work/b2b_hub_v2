import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import (
    start,
    new_application,
    different_types,
)
from constants import TELEGRAM_TOKEN
from logging_config import setup_logging

setup_logging("app.log")
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(different_types.router)
    dp.include_router(new_application.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Приложение запущено")
    asyncio.run(main())
