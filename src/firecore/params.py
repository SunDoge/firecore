from typing import Any
from torch import nn


def get_all(model: nn.Module):
    return model.parameters()


def filter_by_prefix(model: nn.Module, prefix: str):
    for key, value in model.named_parameters():
        if key.startswith(prefix):
            yield value
