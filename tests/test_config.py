from firecore._config import add_arguments
from pydantic import BaseModel
import argparse


def test_add_bool():
    class Options(BaseModel):
        foo: bool = True

    parser = argparse.ArgumentParser()
    add_arguments(parser, Options())
    ns = parser.parse_args(["--foo"])
    assert ns.foo
    ns = parser.parse_args(["--no-foo"])
    assert not ns.foo
