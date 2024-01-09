import argparse
from argparse import ArgumentParser, Namespace
import dataclasses


class BaseArgument:
    @classmethod
    def add_arguments(cls, parser: ArgumentParser, prefix: str = ""):
        for key, value in cls.__dataclass_fields__.items():
            value: dataclasses.Field
            key: str

            parser.add_argument(
                "--{}{}".format(prefix + "-" if prefix else "", key.replace("_", "-")),
                type=value.type,
                default=value.default,
                dest=(prefix + "_" + key),
                help=f"default: {value.default}",
            )

    @classmethod
    def from_arguments(cls, args: Namespace, prefix: str = ""):
        kwargs = {}
        for key in cls.__annotations__.keys():
            kwargs[key] = getattr(args, prefix + "_" + key)
        return cls(**kwargs)
