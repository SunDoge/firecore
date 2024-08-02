import typing

from firecore.import_utils import require
import functools
from pydantic import TypeAdapter
from loguru import logger

_PrimitiveType = typing.Union[bool, int, float, str, dict, list, None]
_ConfigType = typing.Dict[str, _PrimitiveType]
_config_adapter = TypeAdapter(_ConfigType)

_TYPE_KEY = "_type"


class ObjectPool:
    def __init__(
        self,
        config: _ConfigType,
        parent: typing.Optional["ObjectPool"] = None,
        **kwargs,
    ) -> None:
        self._config = _config_adapter.validate_python(config)
        self._pool: typing.Dict[str, typing.Any] = kwargs
        self._parent = parent

        logger.debug("init pool keys: {}", self._pool.keys())

    def get(self, key: str):
        """
        Args:
            key: key in config
        Returns:
            singleton
        """

        if self._parent is not None and self._parent.contains(key):
            return self._parent.get(key)

        if key in self._pool:
            return self._pool[key]

        if key not in self._config:
            raise Exception(f"{key} not in config with keys {self._config.keys()}")

        value = self._instantiate(self._config[key])
        self._pool[key] = value
        return value

    def _instantiate(self, config: typing.Any):
        if isinstance(config, dict):
            if _TYPE_KEY in config:
                return self._instantiate_python_object(config)
            else:
                return {k: self._instantiate(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._instantiate(x) for x in config]
        elif isinstance(config, str):
            if config.startswith("ref:"):
                return self.get(config.split(":")[1])
            elif config.startswith("import:"):
                return require(config.split(":")[1])
            else:
                return config
        else:
            return config

    def _instantiate_python_object(self, config: dict):
        """
        Create python object
        """
        type_: str = config[_TYPE_KEY]

        kwargs = {}
        for key, value in config.items():
            if key == _TYPE_KEY:
                continue
            kwargs[key] = self._instantiate(value)

        out = None
        if type_.startswith("call:"):
            out = require(type_.split(":")[1])(**kwargs)
        elif type_.startswith("partial:"):
            out = functools.partial(require(type_.split(":")[1]), **kwargs)
        else:
            logger.debug("type {} fallback to call", type_)
            out = require(type_.split(":")[1])(**kwargs)

        return out

    def keys(self):
        return self._pool.keys()

    def is_empty(self):
        return bool(self._config)

    def is_in_config(self, key: str):
        return key in self._config

    def is_in_pool(self, key: str):
        return key in self._pool

    def contains(self, key: str):
        return key in self._pool or key in self._config


def _test():
    config = {
        "linear": {
            "_type": "call:torch.nn.Linear",
            "in_features": 2,
            "out_features": 4,
        },
        "dp": {"_type": "call:torch.nn.DataParallel", "module": "ref:linear"},
    }

    object_pool = ObjectPool(config)
    print("=" * 10)
    print(object_pool.get("dp").module is object_pool.get("linear"))
    print(object_pool.keys())


if __name__ == "__main__":
    _test()
