from logging import getLogger

from aiogram import Bot, Dispatcher
import sys


from src.core.config import config
from src.core.db.pool import sqlite_pool
from src.core.logger import setup_logging
from src.handlers import routers


async def init_application() -> tuple[Bot, Dispatcher]:
    setup_logging()
    logger = getLogger(__name__)
    logger.info("Logging configured")

    try:
        logger.info("Filling db connection pool")
        await sqlite_pool.init()
        logger.info("Filling complete")
    except Exception as e:
        logger.error(f"Filling db connection pool failed: {e}")
        sys.exit(1)
    try:
        logger.info("Creating dispatcher")
        dp: Dispatcher = Dispatcher()
    except Exception as e:
        logger.error(f"Creating dispatcher class object failed: {e}")
        sys.exit(1)
    try:
        logger.info("Include routers")
        dp.include_routers(routers)
        logger.info("Complete creating dispatcher")
    except Exception as e:
        logger.error(f"Include routers failed: {e}")
        sys.exit(1)
    try:
        logger.info("Creating bot")
        bot: Bot = Bot(token=config.bot.token, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Creating bot failed: {e}")
        sys.exit(1)
    try:
        logger.info("Deleting webhook")
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Deleting webhook failed: {e}")
        sys.exit(1)

    return bot, dp
