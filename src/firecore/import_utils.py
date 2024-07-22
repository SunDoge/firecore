import importlib
import logging


logger = logging.getLogger(__name__)


def require(name: str):
    """
    import anything by name
    """
    module_name, _sep, attribute_name = name.rpartition('.')
    module = importlib.import_module(module_name)
    attribute = getattr(module, attribute_name)
    logger.debug('import `%s` from `%s`', attribute_name, module_name)
    return attribute
