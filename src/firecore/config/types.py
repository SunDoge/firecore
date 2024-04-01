from typing import Dict, TypedDict
from .lazy import LazyNode


class Loader(LazyNode):
    batch_size: int
    num_workers: int


class Train(TypedDict):
    loader: Loader


class Val(TypedDict):
    loader: Loader


class Test(Val):
    pass


class Strategy(TypedDict):
    max_epochs: int
    epoch_length: int | None


class Config(TypedDict):
    model: LazyNode
    params: LazyNode
    optimizer: LazyNode
    lr_scheduler: LazyNode

    strategy: Strategy

    train: Train | None
    val: Val | None
    test: Test | None
