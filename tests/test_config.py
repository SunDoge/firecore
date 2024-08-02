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
    assert config.val is not None
    assert config.test is None

    config = Config.from_files(
        ["tests/configs/exp001.jsonnet", "tests/configs/patches/server.jsonnet"]
    )
    assert config.test is not None
    assert config.test["hello"] == "world"
    assert config.val is not None
    assert config.train is not None


def test_parent():
    config = Config.from_files(
        ["tests/configs/exp001.jsonnet", "tests/configs/patches/local.jsonnet"]
    )
    object_pools = config.build_object_pools(xx="yy")
    assert object_pools.train.get("xx") == "yy"
    assert object_pools.test.get("xx") == "yy"
    assert object_pools.val.get("xx") == "yy"
    assert object_pools.train.get("max_epochs") == 100
