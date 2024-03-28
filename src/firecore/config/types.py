from typing import Dict, TypedDict


class Loader(TypedDict):
    batch_size: int
    num_workers: int


class Train(TypedDict):
    loader: Loader


class Val(TypedDict):
    loader: Loader


class Config(TypedDict):
    model: Dict
    params: Dict
    optimizer: Dict
    lr_scheduler: Dict

    train: Train | None
    val: Val | None
