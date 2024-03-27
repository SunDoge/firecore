from typing import Any
from torch import nn


def get_all(model: nn.Module):
    return model.parameters()


class AllParams:
    def __call__(self, model: nn.Module) -> Any:
        return model.parameters()
