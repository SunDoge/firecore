import importlib
from loguru import logger
import functools


@functools.lru_cache(maxsize=128)
def require(name: str):
    """
    import anything by name
    """
    module_name, _sep, attribute_name = name.rpartition(".")
    module = importlib.import_module(module_name)
    attribute = getattr(module, attribute_name)
    logger.debug(f"import `{attribute_name}` from `{module_name}`")
    return attribute
