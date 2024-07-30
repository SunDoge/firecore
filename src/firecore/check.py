import argparse
from loguru import logger
import firecore
from pathlib import Path


def make_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    configure_config_command(subparsers.add_parser("config"))

    return parser


def configure_config_command(parser: argparse.ArgumentParser):
    parser.set_defaults(func=config_command)
    parser.add_argument("-c", "--config", type=Path, action="append", required=True)


def config_command(args):
    configs = args.config
    config = firecore.config.load_files([str(f) for f in configs])
    print(config)


def main():
    parser = make_parser()
    args = parser.parse_args()
    logger.info("args: {}", args)
    args.func(args)


if __name__ == "__main__":
    main()
