import importlib.util
from .lazy import Node


def evaluate_file(path: str):
    spec = importlib.util.spec_from_file_location("_firecore_config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate_config(path: str):
    module = evaluate_file(path)
    return getattr(module, "config")


def _is_node(x):
    return isinstance(x, dict) and "path" in x and "args" in x and "kwargs" in x


def _to_node(x):
    if _is_node(x):
        args = x["args"]
        if args is not None:
            args = [_to_node(v) for v in args]

        kwargs = x["kwargs"]
        if kwargs is not None:
            kwargs = {k: _to_node(v) for k, v in kwargs.items()}

        return Node(path=x["path"], args=args, kwargs=kwargs)

    return x


def dict_to_config(x: dict):
    return _to_node(x)


if __name__ == "__main__":
    import sys
    import rich

    import rtoml

    config: Node = evaluate_config(sys.argv[1])
    rich.print(config)
    rich.print(dict_to_config(config.model_dump()))
