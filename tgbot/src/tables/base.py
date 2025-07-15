from abc import ABC, abstractmethod

from aiosqlite import Connection

from src.utils.case_converter import camel_case_to_snake_case


class Base(ABC):
    __tablename__: str

    def __init_subclass__(cls, **kwargs: dict) -> None:
        super().__init_subclass__(**kwargs)
        cls.__tablename__ = camel_case_to_snake_case(cls.__name__)


    def __init__(self, session: Connection) -> None:
        self._session = session

    # noinspection PyPropertyDefinition
    @classmethod
    def get_name(cls) -> str:
        return cls.__tablename__

    @abstractmethod
    async def create(self) -> None:
        """Create a table in the database if it doesn't exist."""

