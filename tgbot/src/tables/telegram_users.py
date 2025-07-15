from dataclasses import field

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

@dataclass(frozen=True)
class TelegramUserInputDTO:
    user_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None
    language_code: str | None
    added_date: str

@dataclass(frozen=True)
class TelegramUserDTO:
    id: int
    user_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None
    language_code: str | None
    added_date: str = field(compare=False, hash=False)

    @classmethod
    def from_input(cls, row_id: int, input_dto: TelegramUserInputDTO) -> "TelegramUserDTO":
        return cls(
            id=row_id,
            user_id=input_dto.user_id,
            is_bot=input_dto.is_bot,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
            username=input_dto.username,
            language_code=input_dto.language_code,
            added_date=input_dto.added_date,
        )
