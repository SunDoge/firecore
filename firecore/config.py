from rjsonnet import evaluate_file, evaluate_snippet
import json
from typing import Dict, Any, Union




def from_file(filename: str, **kwargs) -> Dict[str, Any]:
    json_str = evaluate_file(filename, **kwargs)
    config = json.loads(json_str)
    return config


def from_snippet(expr: str, filename: str = 'snippet.jsonnet', **kwargs) -> Dict[str, Any]:
    json_str = evaluate_snippet(filename, expr, **kwargs)
    config = json.loads(json_str)
    return config
