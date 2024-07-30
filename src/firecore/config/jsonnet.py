from rjsonnet import evaluate_snippet
import typing
from loguru import logger
import json


def eval_files(files: typing.List[str]):
    snippets = ["(import '{}')".format(file) for file in files]
    snippet = "+".join(snippets)
    logger.debug("snippet: `{}`", snippet)
    config = evaluate_snippet("snippet.jsonnet", snippet)
    return config


def load_files(files: typing.List[str]):
    return json.loads(eval_files(files))


if __name__ == "__main__":
    print(
        load_files(
            ["examples/mnist/train_config.jsonnet", "examples/mnist/local.jsonnet"]
        )
    )
