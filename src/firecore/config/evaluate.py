import importlib.util
from .lazy import instantiate


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

    import rtoml

    config: dict = evaluate_config(sys.argv[1])
    rich.print(config)
    rich.print(instantiate(config))
    print(rtoml.dumps(config))

    outs = instantiate(config)
    model = outs['model']
    params = outs['params'](model)
    optimizer = outs['optimizer'](params)
    lr_scheduler = outs['lr_scheduler'](optimizer)
    print(model, params, optimizer, lr_scheduler)