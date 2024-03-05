from firecore._config import add_arguments, assign_arguments
from pydantic import BaseModel
import argparse
import enum


def test_add_bool():
    class Options(BaseModel):
        foo: bool = True

    parser = argparse.ArgumentParser()
    add_arguments(parser, Options())
    ns = parser.parse_args(["--foo"])
    assert ns.foo
    ns = parser.parse_args(["--no-foo"])
    assert not ns.foo


def test_add_int():
    class Options(BaseModel):
        foo: int = 1

    parser = argparse.ArgumentParser()
    add_arguments(parser, Options())
    ns = parser.parse_args(["--foo", "2"])
    assert ns.foo == 2


def test_add_enum():
    class Options(BaseModel):
        class Data(enum.Enum):
            v1 = "123"
            v2 = "234"

        data: Data = Data.v1

    parser = argparse.ArgumentParser()
    add_arguments(parser, Options())
    ns = parser.parse_args([])
    assert ns.data == Options.Data.v1
    ns = parser.parse_args(["--data", "v2"])
    assert ns.data == Options.Data.v2


def test_prefix():
    class Options(BaseModel):
        foo: str = "123"

    prefix = "CFG."

    parser = argparse.ArgumentParser()
    add_arguments(parser, Options(), dest_prefix=prefix)
    ns = parser.parse_args(["--foo", "321"])
    d = assign_arguments(Options().model_dump(), ns.__dict__, dest_prefix=prefix)
    opt = Options.model_validate(d)
    assert opt.foo == "321"


def help_enum():
    class Options(BaseModel):
        class Data(enum.Enum):
            v1 = "123"
            v2 = "234"

        data: Data = Data.v1

    parser = argparse.ArgumentParser()
    add_arguments(parser, Options())
    ns = parser.parse_args()
    d = assign_arguments(Options().model_dump(), ns.__dict__)
    opt = Options.model_validate(d)
    print(opt)


def help_prefix():
    class Options(BaseModel):
        foo: str = "123"

    prefix = "CFG."

    parser = argparse.ArgumentParser()
    add_arguments(parser, Options(), dest_prefix=prefix)
    ns = parser.parse_args()
    print(ns)
    d = assign_arguments(Options().model_dump(), ns.__dict__, dest_prefix=prefix)
    opt = Options.model_validate(d)
    print(opt)


if __name__ == "__main__":
    # help_enum()
    help_prefix()
