from loguru import logger

try:
    import torch
except ImportError:
    logger.exception("please install pytorch first")


from . import optimizer_utils
from . import jit_utils
