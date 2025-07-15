from collections.abc import AsyncGenerator, Awaitable, Callable

from aiosqlite import Connection

from src.tables.integration_ai import IntegrationAI, IntegrationAIDTO, IntegrationAIInputDTO

from .base import AbstractRepository


class LLMRepository(AbstractRepository):
    def __init__(self, db_session_factory: Callable[[], Awaitable[AsyncGenerator[Connection]]]) -> None:
        super().__init__(db_session_factory, IntegrationAI)

    async def get(self, **kwargs: dict[str, int | str]) -> IntegrationAIDTO | None:
        if len(kwargs) != 1:
            raise ValueError("'kwargs' must have exactly 1 argument")

        column, value = next(iter(kwargs.items()))
        valid_fields = IntegrationAIDTO.__annotations__.keys()

        if column not in valid_fields:
            raise ValueError(f"Invalid column name: {column}")

        query = f"SELECT * FROM {self._table_name} WHERE {column} = ? LIMIT 1"
        async with self._db_session_factory() as session:
            result = await session.execute(query, (value, ))
            row = await result.fetchone()
        return IntegrationAIDTO(**dict(row)) if row else None

    async def add(self, dto: IntegrationAIInputDTO) -> IntegrationAIDTO:
        query = (f"""
        INSERT INTO {self._table_name} (
            creator_id, url, auth_type,
            auth_creds, http_method
        ) VALUES (?, ?, ?, ?, ?)
        RETURNING *
        """)
        async with self._db_session_factory() as session:
            result = await session.execute(
                sql=query,
                parameters=(
                    dto.creator_id,
                    dto.url,
                    dto.auth_type,
                    dto.auth_creds,
                    dto.http_method,
                ),
            )
            row = await result.fetchone()
            await session.commit()
        return IntegrationAIDTO(**dict(row))

    async def list(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> list[IntegrationAIDTO | None]:
        query = f"SELECT * FROM {self._table_name} ORDER BY id LIMIT ? OFFSET ?"
        async with self._db_session_factory() as session:
            result = await session.execute(query, (limit, offset))
            rows = await result.fetchall()
        return [IntegrationAIDTO(**dict(row)) for row in rows] if rows else []

    async def delete(self, row_id: int) -> IntegrationAIDTO | None:
        query = f"DELETE FROM {self._table_name} WHERE id = ? RETURNING *"
        async with self._db_session_factory() as session:
            result = await session.execute(query, (row_id,))
            row = await result.fetchone()
            await session.commit()
        return IntegrationAIDTO(**dict(row)) if row else None

    async def update(self, dto: IntegrationAIDTO) -> IntegrationAIDTO | None:
        query = (f"""
                UPDATE {self._table_name}
                SET id = ?
                    creator_id = ?
                    url = ?
                    auth_type = ?
                    auth_creds = ?
                    http_method = ?
                WHERE id = ?
                RETURNING *
        """)
        async with self._db_session_factory() as session:
            result = await session.execute(
                sql=query,
                parameters=(
                    dto.creator_id,
                    dto.url,
                    dto.auth_type,
                    dto.auth_creds,
                    dto.http_method,
                ),
            )
            row = await result.fetchone()
            await session.commit()
        return IntegrationAIDTO(**dict(row)) if row else None
