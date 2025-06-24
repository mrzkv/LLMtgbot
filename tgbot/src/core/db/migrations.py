from src.tables import tables
from aiosqlite import Connection


class Migration:
    def __init__(self, session: Connection):
        self._session = session

    async def create_all(self) -> None:
        for table in tables:
            await table(self._session).create()
        await self._session.commit()

    async def drop_all(self) -> None:
        for table in tables:
            table_name = table.get_name()
            await self._session.execute(f"DROP TABLE IF EXISTS {table_name};")
        await self._session.commit()
