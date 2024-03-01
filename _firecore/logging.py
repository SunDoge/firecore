import logging
from typing import Optional
import sys

logger = logging.getLogger(__name__)

# _MODULE = '{module:s}:{funcName:s}:{lineno:d}'

# FORMAT = '{asctime:s} | {levelname:8s} | {message:s}'

FORMAT = '{asctime:s} | {levelname:8s} | {module:s}:{funcName:s}:{lineno:d} - {message:s}'


def init(filename: Optional[str] = None, local_rank: int = 0, level: int = logging.INFO):

    formatter = logging.Formatter(fmt=FORMAT, style='{')

    handlers = []

    if local_rank == 0:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    if filename:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # log exceptions
    sys.excepthook = handle_exception

    logging.basicConfig(
        level=level,
        force=True,
        handlers=handlers
    )


def handle_exception(exc_type, exc_value, traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, traceback)
        return

    logger.exception(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, traceback)
    )


if __name__ == '__main__':
    init()
    logger.info("test it")
