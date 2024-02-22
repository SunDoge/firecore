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
    parser.add_argument("-n", "--name", type=str, required=True)


def load_or_parse_config(
    ns: argparse.Namespace, model_class: Type[ModelType]
) -> ModelType:
    config_path: Optional[Path] = ns.config
    if config_path is not None:
        with config_path.open("r") as f:
            parsed_config = rtoml.load(f)
    else:
        parsed_config = model_class().model_dump()

    assign_arguments(parsed_config, ns.__dict__, prefix="CFG.")

    config = model_class.model_validate(parsed_config)
    return config


@contextmanager
def start_training(model_class: Type[ModelType]):
    parser = argparse.ArgumentParser()
    configure_argument_parser(parser)
    add_arguments(parser, model_class(), dest_prefix="CFG")

    ns = parser.parse_args()

    working_dir: Path = ns.workdir
    experiment_name: str = ns.name

    config = load_or_parse_config(ns, model_class)

    ctx = Context(
        workdir=working_dir,
        experiment_name=experiment_name,
        started_at=datetime.now(),
        config=config,
    )

    ctx.experiment_dir.mkdir(parents=True, exist_ok=True)

    yield ctx

    ctx.save_config()
