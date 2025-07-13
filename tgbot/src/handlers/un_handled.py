from logging import getLogger

from aiogram import F, Router
from aiogram.types import Message

router = Router()

logger = getLogger(__name__)

@router.message(F.text)
async def un_handled_handler(message: Message) -> None:
    logger.info(f"{message.from_user.username}:{message.from_user.id}:{message.text}")
