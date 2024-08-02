import firecore
from firecore.config.types import Config


def test_basic():
    config = Config.from_files(["tests/configs/exp001.jsonnet"])
    assert config.shared["max_epochs"] == 100


def test_merge():
    config = Config.from_files(
        ["tests/configs/exp001.jsonnet", "tests/configs/patches/local.jsonnet"]
    )
    assert config.train is not None
    assert config.train["hello"] == "world"

    config = Config.from_files(
        ["tests/configs/exp001.jsonnet", "tests/configs/patches/server.jsonnet"]
    )
    assert config.test is not None
    assert config.test["hello"] == "world"
