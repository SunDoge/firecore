from typing import Dict, TypedDict
from .lazy import LazyNode


class Loader(LazyNode):
    batch_size: int
    num_workers: int


class Train(TypedDict):
    loader: Loader


class Val(TypedDict):
    loader: Loader


class Strategy(TypedDict):
    max_epochs: int


class Config(TypedDict):
    model: LazyNode
    params: LazyNode
    optimizer: LazyNode
    lr_scheduler: LazyNode

    strategy: Strategy

    train: Train | None
    val: Val | None
