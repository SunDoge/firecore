import os

KEY = "PY_LOG"


def parse_env(env: str):
    kvs = env.split(",")
    for kv in kvs:
        k, v = kv.split("=")
        yield k, v
