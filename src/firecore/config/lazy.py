from typing import TypeVar, Type, Any, Generic, Literal, List, Dict
from loguru import logger
import functools
import enum
from pydantic import BaseModel


T = TypeVar("T")


class Node(BaseModel):
    path: str
    type: Literal["object", "callable"]
    args: List[Any] | None = None
    kwargs: Dict[str, Any] | None = None

    def __call__(self, *args, **kwargs):
        return Node(path=self.path, type="object", args=args, kwargs=kwargs)


def _get_target_path(target):
    return target.__module__ + "." + target.__name__


def LazyCall(target: T) -> T:
    return Node(path=_get_target_path(target), type="callable")


def main():
    from firecore.opencv import decode_rgb_image
    from firecore.params import AllParams

    cfg: BaseModel = LazyCall(decode_rgb_image)(buf=b"1", c=LazyCall(AllParams))
    print(cfg.model_dump_json())


if __name__ == "__main__":
    main()
