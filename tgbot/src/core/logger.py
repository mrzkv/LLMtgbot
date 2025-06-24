from pathlib import Path
from sys import stdout

from loguru import logger


def setup_logging() -> None:
    log_path = Path("tgbot/data/logs/bot.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sink=stdout,
        level="DEBUG",
        format="<green>{time:HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True,
    )

    logger.add(
        str(log_path),
        level="INFO",
        rotation="1 MB",
        retention="10 days",
        compression="zip",
        encoding="utf-8",
        enqueue=True,
    )
