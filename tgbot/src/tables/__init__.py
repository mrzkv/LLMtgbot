from .base import Base  #  noqa: F401
from .integration_ai import IntegrationAI
from .telegram_users import TelegramUser

tables = [
    IntegrationAI,
    TelegramUser,
]
