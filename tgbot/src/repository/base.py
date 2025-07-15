from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Awaitable, Callable
from typing import TypeVar

from aiosqlite import Connection

from src.tables.base import Base

T = TypeVar("T")
TableType = TypeVar("TableType", bound=Base)

class AbstractRepository(ABC):
    def __init__(
            self,
            db_session_factory: Callable[[],Awaitable[AsyncGenerator[Connection]]],
            table_class: TableType,
    ) -> None:
        self._db_session_factory = db_session_factory
        self._table_name = table_class.get_name()

    @abstractmethod
    async def get(self, **kwargs: dict) -> T | None:
        """This function takes positional arguments
        and executes the query with them.
        """

    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[T]:
        pass

    @abstractmethod
    async def add(self, obj: T) -> T:
        pass

    @abstractmethod
    async def delete(self, obj_id: int) -> T:
        pass
