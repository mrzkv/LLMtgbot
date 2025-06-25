from .base import Base
from dataclasses import dataclass

class TelegramUser(Base):
    async def create(self) -> None:
        await self._session.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.__tablename__} (
                id              INTEGER PRIMARY KEY AUTOINCREMENT, -- ID строки
                user_id         BIGINT NOT NULL,                   -- Telegram ID пользователя
                is_bot          BOOLEAN NOT NULL,                  -- Является ли ботом
                first_name      TEXT,                              -- Имя
                last_name       TEXT,                              -- Фамилия
                username        TEXT,                              -- Username
                language_code   TEXT,                              -- Язык интерфейса Telegram
                added_date      TEXT NOT NULL                      -- ISO 8601 timestamp (например, "2025-06-25T13:45:00Z")
        );
    """)

@dataclass
class TelegramUserInputDTO:
    user_id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str
    added_date: str

    def __post_init__(self) -> None:
        if type(self.user_id) is not int:
            raise TypeError("user_id must be int")
        if type(self.is_bot) is not bool:
            raise TypeError("is_bot must be bool")
        if type(self.first_name) is not str:
            raise TypeError("first_name must be str")
        if type(self.last_name) is not str:
            raise TypeError("last_name must be str")
        if type(self.language_code) is not str:
            raise TypeError("language_code must be str")
        if type(self.added_date) is not str:
            raise TypeError("added_date must be str")

@dataclass
class TelegramUserDTO:
    id: int
    user_id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str
    added_date: str