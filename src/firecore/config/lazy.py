from typing import TypeVar, Any, List, Dict
from loguru import logger
from pydantic import BaseModel
import importlib
import functools
import importlib.util


@functools.lru_cache(maxsize=128)
def require(name: str):
    """
    import anything by name
    """
    module_name, _sep, attribute_name = name.rpartition(".")
    module = importlib.import_module(module_name)
    attribute = getattr(module, attribute_name)
    logger.debug("import {} from {}", attribute_name, module_name)
    return attribute


def _instantiate_if_is_node(x, recursive: bool):
    if isinstance(x, Node):
        return x.instantiate(recursive=recursive)
    else:
        return x


class Node(BaseModel):
    path: str
    args: List[Any] | None = None
    kwargs: Dict[str, Any] | None = None

    def __call__(self, *args, **kwargs):
        return Node(path=self.path, args=args, kwargs=kwargs)

    @property
    def is_callable(self):
        return self.args is None and self.kwargs is None

    @property
    def target(self):
        return require(self.path)

    def instantiate(self, recursive: bool = True):
        if recursive:
            args = [_instantiate_if_is_node(x, recursive=recursive) for x in self.args]
            kwargs = {
                k: _instantiate_if_is_node(v, recursive=recursive)
                for k, v in self.kwargs.items()
            }
        else:
            args = self.args
            kwargs = self.kwargs
        return self.target(*args, **kwargs)


def _get_target_path(target):
    return target.__module__ + "." + target.__name__


T = TypeVar("T")


def LazyCall(target: T) -> T:
    return Node(path=_get_target_path(target))


def main():
    from firecore.opencv import decode_rgb_image
    from firecore.params import AllParams
    import rtoml

    cfg: Node = LazyCall(decode_rgb_image)(buf=b"1", c=LazyCall(AllParams))
    print(rtoml.dumps(cfg.model_dump(exclude_unset=True)))
    print(cfg.target)


if __name__ == "__main__":
    main()
