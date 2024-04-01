from typing import Callable, Optional, TypeVar, Union
import inspect
import importlib.util


T = TypeVar("T")


def _main_fn(func: T) -> T:
    # 拿到调用这个函数的 FrameInfo
    caller = inspect.stack()[2]
    # import ipdb; ipdb.set_trace()
    # 拿到 __name__
    name = caller.frame.f_globals["__name__"]

    if name == "__main__":
        file_path = caller.frame.f_globals["__file__"]
        spec = importlib.util.spec_from_file_location("__fake_main", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        getattr(module, func.__name__)()
    else:
        return func


def main_fn(func: Optional[T]) -> Union[Callable[[T], T], T]:
    if func:
        return _main_fn(func)
    else:
        return _main_fn
