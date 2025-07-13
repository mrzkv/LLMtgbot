from ast import literal_eval
from dataclasses import dataclass, field
from logging import getLevelNamesMapping
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    token: str # Telegram bot token
    admin_ids: list[int] = field(default_factory=list)

@dataclass
class LogConfig:
    level: str
    level_value: int = field(init=False)

    def __post_init__(self) -> None:
        self.level_value = getLevelNamesMapping().get(self.level, 10)  # default DEBUG



@dataclass
class DBConfig:
    path: str
    pool_size: int
    max_overflow: int

@dataclass
class AppConfig:
    bot: BotConfig
    log: LogConfig
    db: DBConfig

config: AppConfig = AppConfig(
    bot=BotConfig(
        token=getenv("BOT_TOKEN"),
        admin_ids=literal_eval(getenv("BOT_ADMIN_IDS", "[]")),
    ),
    log=LogConfig(
        level=getenv("LOG_LEVEL"),
    ),
    db=DBConfig(
        path=getenv("DB_PATH"),
        pool_size=int(getenv("DB_POOL_SIZE", "2")),
        max_overflow=int(getenv("DB_MAX_OVERFLOW", "1")),
    ),
)

