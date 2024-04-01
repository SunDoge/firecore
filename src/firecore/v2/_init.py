import argparse
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Tuple, List
import rjsonnet


def configure_parser(parser: ArgumentParser | None = None):
    if parser is None:
        parser = ArgumentParser()

    def tla(x: str):
        return tuple(x.split("="))

    parser.add_argument("-c", "--config", type=Path, help="Path to config file.")
    parser.add_argument("--tla-str", nargs=argparse.ONE_OR_MORE, type=tla, default=[])
    parser.add_argument("--tla-code", nargs=argparse.ONE_OR_MORE, type=tla, default=[])

    return parser


def parse_config(args: argparse.Namespace) -> Dict:
    config_path: Path | None = args.config
    tla_str_list: List[Tuple[str, str]] = args.tla_str
    tla_code_list: List[Tuple[str, str]] = args.tla_code

    config = rjsonnet.evaluate_file(
        str(config_path), tla_vars=dict(tla_str_list), tla_codes=dict(tla_code_list)
    )

    return config


if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()
    print(args)
    config = parse_config(args)
    print(config)
