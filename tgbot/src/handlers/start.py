from logging import getLogger

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards.builder import InlineKeyboardFactory
from src.services.user import UserService, UserServiceFactory
from src.text.builder import TextBuilder

router = Router()

logger = getLogger(__name__)

@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    logger.info(f"{message.from_user.id}: started bot")
    await message.answer(
        text=TextBuilder.start_handler(),
        reply_markup=InlineKeyboardFactory.choose_language(),
    )
    service: UserService = UserServiceFactory.create(message)
    await service.add_new_user()
