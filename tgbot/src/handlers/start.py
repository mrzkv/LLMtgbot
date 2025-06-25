from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from logging import getLogger

router = Router()

logger = getLogger(__name__)

@router.message(CommandStart)
async def start_handler(message: Message) -> None:
    logger.info(f"{message.from_user.id}: started bot")
    await message.answer("Hello, world!")
