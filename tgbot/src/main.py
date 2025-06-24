import asyncio

from src.core.lifespan import init_application


async def start_bot() -> None:
    bot, dp = await init_application()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
