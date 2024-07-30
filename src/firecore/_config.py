from pydantic import BaseModel
import argparse
from argparse import ArgumentParser
import typing
from typing import Dict, Any, Type, TypeVar, Optional, Union
from loguru import logger
import enum


_NoneType = type(None)


def add_arguments(
    parser: ArgumentParser,
    model: BaseModel,
    name_prefix: str = "--",
    dest_prefix: str = "",
):
    group = parser.add_argument_group(title=f"{model.__class__.__qualname__}")
    for key, field in model.model_fields.items():
        name = name_prefix + key.replace("_", "-")
        dest = dest_prefix + key

        logger.debug(f"name={name}, dest={dest}, key={key}, field={field}")

        tp = typing.get_origin(field.annotation)

        logger.debug(f"check type: {tp}")

        if tp is None:  # not typing annotation
            if issubclass(field.annotation, BaseModel):
                add_arguments(
                    parser,
                    field.default,
                    name_prefix=name + "-",
                    dest_prefix=dest + ".",
                )
                continue

            if field.annotation is bool:
                # add --flag and --no-flag
                add_bool_argument(group, name, dest, field.default)
                continue

            add_typed_argument(group, name, dest, field.default, field.annotation)
            continue

        if tp is typing.Union:
            inner = typing.get_args(field.annotation)
            if len(inner) == 2 and _NoneType in inner:  # typing.Optional
                tp2 = get_not_none(inner)
                if tp2 is bool:
                    add_bool_argument(group, name, dest, field.default)
                else:
                    add_typed_argument(group, name, dest, field.default, tp2)
                continue

        if tp is list:
            inner = typing.get_args(field.annotation)
            assert len(inner) == 1
            tp2 = inner[0]
            add_typed_list_argument(group, name, dest, field.default, tp2)
            continue


def add_bool_argument(parser: ArgumentParser, name: str, dest: str, default: bool):
    parser.add_argument(
        name,
        action=argparse.BooleanOptionalAction,
        default=default,
        dest=dest,
        help=f"(default: bool = {default})",
    )


T = TypeVar("T")


def add_typed_argument(
    parser: ArgumentParser,
    name: str,
    dest: str,
    default: Optional[T],
    type: Type[T],
):
    if issubclass(type, enum.Enum):
        type = StrToEnum(type)

    parser.add_argument(
        name,
        dest=dest,
        default=default,
        type=type,
        help=f"(default: {type.__name__} = {default})",
    )


def add_typed_list_argument(
    parser: ArgumentParser,
    name: str,
    dest: str,
    default: Optional[T],
    type: Type[T],
):
    parser.add_argument(
        name,
        dest=dest,
        default=default,
        type=type,
        help=f"(default: List[{type.__name__}] = {default})",
        nargs=argparse.ZERO_OR_MORE,
    )


def get_not_none(xs):
    rest = [x for x in xs if x is not _NoneType]
    logger.debug(f"rest: {rest}")
    return rest[0]


def assign_arguments(
    options: Dict[str, Any], parsed: Dict[str, Any], dest_prefix: str = ""
):
    for key, value in parsed.items():
        if not key.startswith(dest_prefix):
            continue

        key = key[len(dest_prefix) :]
        parts = key.split(".")
        # print(parts)
        dict_ref = options
        for part in parts[:-1]:
            dict_ref = dict_ref[part]

        _key = parts[-1]
        if dict_ref[_key] != value:
            logger.info("modify {}: {} => {}", key, dict_ref[_key], value)
            dict_ref[_key] = value

    return options


class StrToEnum:
    def __init__(self, enum_class) -> None:
        self._enum_class = enum_class

    def __call__(self, key: Optional[str]):
        if key is None:
            return None
        else:
            return self._enum_class[key]

    @property
    def __name__(self):
        return self._enum_class.__name__
