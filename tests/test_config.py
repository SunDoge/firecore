import firecore
import functools

FIRECORE_LIBSONNET = 'jsonnet/firecore.libsonnet'


def test_eval_snippet():
    snippet = "{a:1, b:2}"
    expected = dict(a=1, b=2)
    output = firecore.config.from_snippet(snippet)
    assert output == expected




