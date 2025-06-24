from aiogram import Bot, Dispatcher

from src.core.config import config
from src.core.logger import setup_logging
from src.handlers import handlers

setup_logging()

async def start_bot() -> None:
    bot: Bot = Bot(token=config.bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    dp.include_routers(handlers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
