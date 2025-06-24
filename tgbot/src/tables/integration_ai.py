from .base import Base


class IntegrationAI(Base):
    @staticmethod
    def get_name() -> str:
        return self.__tablename__

    async def create(self) -> None:
        await self._session.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.__tablename__} (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id   INTEGER,
                url          TEXT NOT NULL,
                auth_type    INTEGER CHECK(auth_type IN (0, 1, 2)),        
                auth_creds   TEXT,
                http_method  INTEGER CHECK(http_method IN (0, 1, 2, 3))
        );
    """)

