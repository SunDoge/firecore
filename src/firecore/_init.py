import argparse
from typing import Optional, Type, TypeVar, Generic
import rtoml
from pathlib import Path
from pydantic import BaseModel
from ._config import add_arguments, assign_arguments
from loguru import logger
from datetime import datetime
from contextlib import contextmanager

ModelType = TypeVar("ModelType", bound=BaseModel)

DEST_PREFIX = "CFG."


class Context(BaseModel, Generic[ModelType]):
    workdir: Path
    started_at: datetime
    config: ModelType

    @property
    def experiment_dir(self):
        return self.workdir / self.started_at.strftime("%Y-%m-%d-%H-%M-%S")

    def save_config(self):
        path = self.save_dir / "config.toml"
        logger.info("save config to {}", path)
        with path.open("w") as f:
            rtoml.dump(self.config.model_dump(), f)


def configure_argument_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--config", type=Path, help="Path to config file.")
    parser.add_argument(
        "-w", "--workdir", type=Path, default="/tmp", help="Path to working dir."
    )


def load_or_parse_config(
    ns: argparse.Namespace, model_class: Type[ModelType]
) -> ModelType:
    config_path: Optional[Path] = ns.config
    if config_path is not None:
        with config_path.open("r") as f:
            config_dict = rtoml.load(f)
    else:
        config_dict = model_class().model_dump()

    assign_arguments(config_dict, ns.__dict__, dest_prefix=DEST_PREFIX)
    config = model_class.model_validate(config_dict)
    return config


def prepare_parser(
    config_class: Type[ModelType], parser: Optional[argparse.ArgumentParser] = None
):
    if parser is None:
        parser = argparse.ArgumentParser()
    configure_argument_parser(parser)
    add_arguments(parser, config_class(), dest_prefix=DEST_PREFIX)
    return parser


def make_dir_with_index_and_timestamp(root_dir: Path):
    sub_dirs = list(root_dir.iterdir())
    index = len(sub_dirs)


@contextmanager
def start_training(config_class: Type[ModelType]):
    pass
