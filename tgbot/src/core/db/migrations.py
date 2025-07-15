from aiosqlite import Connection

from src.tables import tables


class Migration:
    def __init__(self, session: Connection) -> None:
        self._session = session

    async def create_all(self) -> None:
        for table in tables:
            await table(self._session).create()
        await self._session.commit()

    async def drop_all(self) -> None:
        for table in tables:
            await self._session.execute(f"DROP TABLE IF EXISTS {table.get_name()};")
        await self._session.commit()
