import importlib.util


def evaluate_file(path: str):
    spec = importlib.util.spec_from_file_location("_firecore_config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate_config(path: str):
    module = evaluate_file(path)
    return getattr(module, "config")


if __name__ == "__main__":
    import sys
    import rich
    from .lazy import Node
    import rtoml

    config: Node = evaluate_config(sys.argv[1])
    rich.print(config)
    print(config.model_dump_json(indent=2))
    model_factory = config.kwargs["model_factory"].instantiate(recursive=False)
    print(model_factory.model)
    print(model_factory.optimizer)
    print(model_factory.lr_scheduler)
