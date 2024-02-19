import argparse
from typing import Callable, Optional, Type, TypeVar
import rtoml
from pathlib import Path
from pydantic import BaseModel
from ._config import add_arguments, assign_arguments
from loguru import logger
import inspect


def configure_argument_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--config", type=Path, help="Path to config file.")


T = TypeVar("T", BaseModel)


def load_or_parse_config(ns: argparse.Namespace, model_class: Type[T]) -> T:
    config_path: Optional[Path] = ns.config
    if config_path is not None:
        with config_path.open("r") as f:
            parsed_config = rtoml.load(f)
    else:
        parsed_config = {}

    assign_arguments(parsed_config, ns.__dict__, prefix="CFG.")
    config = model_class.model_validate(parsed_config)
    return config


def start_training(model_class: Type[T], func: Callable[[T]]):
    parser = argparse.ArgumentParser()
    configure_argument_parser(parser)
    add_arguments(parser, model_class(), dest_prefix="CFG.")

    ns = parser.parse_args()
    config = load_or_parse_config(ns, model_class)
    return func(config)
