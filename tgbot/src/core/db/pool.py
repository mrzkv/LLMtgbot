import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiosqlite

from src.core.config import config


class SQlitePool:
    def __init__(
            self,
            db_path: str,
            pool_size: int = 5,
            max_overflow: int = 0
    ) -> None:
        self._db_path = db_path
        self._pool = asyncio.Queue(maxsize=pool_size)
        self._max_overflow = max_overflow

        self._overflow_lock = asyncio.Lock()
        self._overflow = 0
        self._initialized = False


    async def init(self) -> None:
        while not self._pool.full():
            session: aiosqlite.Connection = await aiosqlite.connect(self._db_path)
            session.row_factory = aiosqlite.Row
            await self._pool.put(session)
        self._initialized = True

    async def close(self) -> None:
        while not self._pool.empty():
            session: aiosqlite.Connection = await self._pool.get()
            await session.close()

        self._initialized = False

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[aiosqlite.Connection, None]:
        if not self._initialized:
            raise RuntimeError("Pool must be initialized, call init() first")

        session: aiosqlite.Connection | None = None
        is_overflow = False

        try:
            try:
                session = await self._pool.get_nowait() # Get session from pool
            except asyncio.QueueEmpty:
                async with self._overflow_lock:
                    # If pool empty and _overflow not reached max_overflow, create a new session
                    if self._overflow < self._max_overflow:
                        self._overflow += 1
                        session = await aiosqlite.connect(self._db_path)
                        is_overflow = True # marks the session as overflow_session
                    else:
                        # If _overflow == max_overflow, wait new session
                        session = await self._pool.get()

            session.row_factory = aiosqlite.Row # set return dict, not tuple
            yield session

        finally:
            if session:
                if is_overflow: # check session
                    # if the session is overflow, he doesn't put in asyncio.Queue
                    async with self._overflow_lock:
                        self._overflow -= 1
                    await session.close()
                else:
                    await self._pool.put(session) # put session in asyncio.Queue


sqlite_pool = SQlitePool(
    db_path=config.db.path,
    pool_size=config.db.pool_size,
    max_overflow=config.db.max_overflow
)
