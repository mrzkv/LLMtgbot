import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiosqlite


class SQlitePool:
    def __init__(
            self,
            db_path: str,
            pool_size: int = 5,
    ) -> None:
        self.db_path = db_path
        self._pool = asyncio.Queue(maxsize=pool_size)
        self._initialized = False

    async def init(self) -> None:
        while not self._pool.full():
            session = aiosqlite.connect(self.db_path)
            session.row_factory = aiosqlite.Row
            await self._pool.put(session)
        self._initialized = True

    async def close(self) -> None:
        while not self._pool.empty():
            session = self._pool.get()
            await session.close()
        self._initialized = False

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[aiosqlite.Connection]:
        if not self._initialized:
            raise RuntimeError("Pool must be initialized, call init() first")
        session = await self._pool.get()
        try:
            yield session
        finally:
            await self._pool.put(session)
