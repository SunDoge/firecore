from typing import Callable, Optional, TypeVar, Dict
import functools
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class AutoConfig:
    def __init__(self, **kwargs) -> None:
        self._kwargs = kwargs

    def __call__(
        self, target: T, index: Optional[int] = None, prefix: Optional[str] = None
    ) -> T:
        target_name: str = getattr(target, "__name__")
        if prefix:
            target_name = prefix + target_name
        if index:
            target_name = target_name + str(index)

        cfg: Dict = self._kwargs.get(target_name, {})
        logger.debug(f"target name: {target_name} with cfg: {cfg}")

        def f(**kwargs) -> T:
            kwargs.update(cfg)
            return target(**kwargs)

        return f

    def get(self, key: str, default=None):
        return self._kwargs.get(key, default)


def auto_config(func):
    @functools.wraps(func)
    def f(**kwargs):
        return func(AutoConfig(**kwargs))

    return f
