from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):

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
