import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiosqlite

from src.core.config import config


class SQlitePool:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    @asynccontextmanager
    async def get_async_session(self):
        session = await aiosqlite.connect(self._db_path)
        session.row_factory = aiosqlite.Row
        try:
            yield session
        finally:
            await session.close()


sqlite_pool = SQlitePool(db_path=config.db.path)
