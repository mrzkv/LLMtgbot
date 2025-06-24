import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import stdout


def setup_logging() -> None:
    log_path = Path("data/logs/bot.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    date_format = "%H:%M:%S"

    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=1 * 1024 * 1024,  # 1 MB
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
