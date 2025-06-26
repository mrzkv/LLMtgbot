
from pydantic.dataclasses import dataclass

from .base import Base


class TelegramUser(Base):
    async def create(self) -> None:
        await self._session.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.__tablename__} (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         BIGINT NOT NULL,
                is_bot          BOOLEAN NOT NULL,
                first_name      TEXT,
                last_name       TEXT,
                username        TEXT,
                language_code   TEXT,
                added_date      TEXT NOT NULL
        );
    """)

@dataclass
class TelegramUserInputDTO:
    user_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None
    language_code: str | None
    added_date: str

@dataclass
class TelegramUserDTO: # noqa: PLW1641
    id: int
    user_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None
    language_code: str | None
    added_date: str

    @classmethod
    def from_input(cls, row_id: int, input_dto: TelegramUserInputDTO) -> "TelegramUserDTO":
        return cls(id=row_id, **vars(input_dto))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TelegramUserDTO):
            return False

        ignore_fields = {"added_date"}

        for field in self.__dataclass_fields__:
            if field in ignore_fields:
                continue
            if getattr(self, field) != getattr(other, field):
                return False
        return True
