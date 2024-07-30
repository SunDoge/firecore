from firecore.global_store import GLOBAL_STORE
from typing import Dict, Type, TypeVar
from pydantic import TypeAdapter
import functools


T = TypeVar("T")


class _Missing:
    pass


_MISSING = _Missing()


def _get_by_path(nested: Dict, path: str):
    keys = path.split(".")
    result = nested
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        elif isinstance(result, list) and key.isdecimal():
            result = result[int(key)]
        else:
            if key is keys[-1]:
                return _MISSING
            else:
                raise KeyError(f"fail to get {key} from path {path}")
    return result


@functools.lru_cache(maxsize=1024)
def _get_type_adapter(type):
    return TypeAdapter(type)


def config(key: str, type: Type[T], default: T | _Missing = _MISSING) -> T:
    conf: Dict = GLOBAL_STORE.get("config")
    value = _get_by_path(conf, key)

    if value is _MISSING and default is not _MISSING:
        value = default

    adapter: TypeAdapter = _get_type_adapter(type)
    return adapter.validate_python(value)


if __name__ == "__main__":
    GLOBAL_STORE.set("config", {"a": {"b": 1, "c": {}, "d": [1]}})
    out = config("a.b", int)
    print(out)
    out = config("a.c", Dict)
    print(out)
    out = config("a", Dict)
    print(out)
    out = config("a.d.0", int)
    print(out)
