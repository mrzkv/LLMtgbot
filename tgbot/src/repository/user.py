from .base import AbstractRepository
from aiosqlite import Connection

from src.tables.telegram_users import TelegramUserDTO, TelegramUser, TelegramUserInputDTO
from dataclasses import fields

class UserRepository(AbstractRepository[TelegramUserDTO]):
    def __init__(
            self,
            session: Connection,
    ) -> None:
        self._session = session

    async def get(self, **kwargs: dict[str, int | str]) -> TelegramUserDTO | None:
        if len(kwargs) != 1:
            raise ValueError("'kwargs' must have exactly 1 argument")

        column, value = next(iter(kwargs.items()))
        valid_fields = TelegramUser.__annotations__.keys()

        if column not in valid_fields:
            raise ValueError(f"Invalid column name: {column}")

        query = f"SELECT * FROM {TelegramUser.__tablename__} WHERE {column} = ? LIMIT 1"
        result = await self._session.execute(query, (value,))
        row = await result.fetchone()
        if not row:
            return None
        return TelegramUserDTO(**dict(row))

    async def add(self, dto: TelegramUserInputDTO) -> TelegramUserDTO:
        query = (f"""
        INSERT INTO {TelegramUser.__tablename__} (
            user_id, is_bot, first_name, last_name,
            username, language_code, added_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING *""")

        result = await self._session.execute(
            sql=query,
            parameters=(
                dto.user_id,
                dto.is_bot,
                dto.first_name,
                dto.last_name,
                dto.username,
                dto.language_code,
                dto.added_date,
            )
        )
        row = await result.fetchone()
        return TelegramUserDTO(**dict(row))

    async def list(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> list[TelegramUserDTO]:
        query = f"SELECT * FROM {TelegramUser.__tablename__} ORDER BY id LIMIT ? OFFSET ?"
        result = await self._session.execute(query, (limit, offset))
        rows = await result.fetchall()
        return [TelegramUserDTO(**dict(row)) for row in rows]

    async def delete(self, row_id: int) -> TelegramUserDTO | None:
        query = f"DELETE FROM {TelegramUser.__tablename__} WHERE id = ? RETURNING *"
        result = await self._session.execute(query, (row_id,))
        row = await result.fetchone()
        if not row:
            return None
        return TelegramUserDTO(**dict(row))

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

