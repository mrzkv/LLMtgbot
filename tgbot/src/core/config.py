from dataclasses import dataclass, field
from logging import getLevelNamesMapping
from os import getenv
from ast import literal_eval

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    token: str # Telegram bot token
    admin_ids: list[int] = field(default_factory=list)

@dataclass
class LogConfig:
    level: str
    @property
    def level_value(self) -> int:
        return getLevelNamesMapping().get(self.level)


@dataclass
class DBConfig:
    driver: str
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def async_url(self) -> str:
        if self.driver == "sqlite":
            return f"sqlite+aiosqlite:///{self.database}"

        return f"{self.driver}+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class AppConfig:
    bot: BotConfig
    log: LogConfig


config = AppConfig(
    bot=BotConfig(
        token=getenv("BOT_TOKEN"),
        admin_ids=literal_eval(getenv("BOT_ADMIN_IDS", "[]"))
    ),
    log=LogConfig(
        level=getenv("LOG_LEVEL"),
    ),
)
