from firecore import jsonnet_loader
import json


def test_eval_snippet():
    snippet = "{a:1, b:2}"
    expected = dict(a=1, b=2)
    output = jsonnet_loader.evaluate_snippet("snippet", snippet)
    output = json.loads(output)
    assert output == expected
