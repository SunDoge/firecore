from typing import Dict, Any, Callable, Optional, List, Union
import functools

StrMapping = Dict[str, str]


def adapt(
    inputs: Dict[str, Any], rules: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    outputs = inputs
    # Not None and not empty dict
    if rules:
        # outputs = {new_key: inputs[old_key] for new_key, old_key in rules.items()}
        outputs = {new_key: inputs[key] for key, new_key in rules.items()}
    return outputs


class Adapter:
    def __init__(
        self, in_rules: Dict[str, str] = {}, out_rules: Dict[str, str] = {}
    ) -> None:
        self._in_rules = in_rules
        self._out_rules = out_rules

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def f(**kwargs) -> Dict[str, Any]:
            new_kwargs = adapt(kwargs, self._in_rules)
            outputs = func(**new_kwargs)
            assert isinstance(outputs, dict)
            new_outputs = adapt(outputs, self._out_rules)
            return new_outputs

        return f


def extract(
    input_dict: dict, rules: List[str]
):
    return [input_dict[k] for k in rules]


def nameing(
    input_list: list, rules: List[str]
):
    if not isinstance(input_list, (list, tuple)):
        input_list = [input_list]
    assert len(input_list) == len(
        rules), f'{len(input_list)} and {len(rules)} is not same'
    return {k: v for k, v in zip(rules, input_list)}
