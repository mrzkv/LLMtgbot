from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.core.config import config
from src.core.db.migrations import Migration
from src.core.db.pool import sqlite_pool
from src.core.logger import setup_logging
from src.handlers import routers


@asynccontextmanager
async def init_application() -> AsyncGenerator[tuple[Bot, Dispatcher]]:
    setup_logging()
    logger = getLogger(__name__)
    logger.info("Logging configured")

    bot = None
    dp = None

    try:
        logger.info("Creating tables")
        async with sqlite_pool.get_async_session() as session:
            await Migration(session).create_all()
        logger.info("Tables created")

        logger.info("Creating bot")
        bot = Bot(
            token=config.bot.token,
            default=DefaultBotProperties(parse_mode="HTML"),
        )

        logger.info("Creating dispatcher")
        dp = Dispatcher()

        logger.info("Include routers")
        dp.include_routers(*routers)

        logger.info("Deleting webhook")
        await bot.delete_webhook(drop_pending_updates=True)

        yield bot, dp

    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        raise

    finally:
        if dp:
            try:
                logger.info("Closing dispatcher storage")
                await dp.storage.close()
            except Exception as e:
                logger.error(f"Closing dispatcher storage failed: {e}")

        if bot:
            try:
                logger.info("Closing bot session")
                await bot.session.close()
            except Exception as e:
                logger.error(f"Closing bot session failed: {e}")

        try:
            logger.info("Closing db connection pool")
            await sqlite_pool.close()
        except Exception as e:
            logger.error(f"Closing db connection pool failed: {e}")
