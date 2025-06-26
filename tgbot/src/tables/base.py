from abc import ABC, abstractmethod

from aiosqlite import Connection

from src.utils.case_converter import camel_case_to_snake_case


class Base(ABC):
    def __init__(self, session: Connection) -> None:
        self._session = session
        self.__tablename__ = camel_case_to_snake_case(self.__class__.__name__)

    @classmethod
    def get_table_name(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)

    @abstractmethod
    async def create(self) -> None:
        """Create a table in the database if it doesn't exist."""

