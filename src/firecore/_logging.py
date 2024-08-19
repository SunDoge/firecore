from loguru import logger
from pathlib import Path
import logging
import inspect
from pydantic import BaseModel

logger.disable("firecore")


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_std_logger():
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


class LoguruConfig(BaseModel):
    pass


def setup_logger():
    configure_std_logger()
    logger.configure()
