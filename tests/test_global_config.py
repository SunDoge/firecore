from firecore.global_config import config
from firecore.global_store import GLOBAL_STORE
from typing import Dict


def test_set_config():
    GLOBAL_STORE.set("config", {"a": {"b": 1, "c": {}, "d": [1]}})
    out = config("a.b", int)
    assert out == 1
    out = config("a.c", Dict)
    assert out == {}
    out = config("a", Dict)
    assert isinstance(out, dict)
    out = config("a.d.0", int)
    assert out == 1
