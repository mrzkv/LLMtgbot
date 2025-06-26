from logging import getLogger

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.services.user import UserService, UserServiceFactory

router = Router()

logger = getLogger(__name__)

@router.message(CommandStart)
async def start_handler(message: Message) -> None:
    logger.info(f"{message.from_user.id}: started bot")
    service: UserService = await UserServiceFactory.create(message)
    ans = await service.add_new_user()
    await message.answer(f"{ans}")
