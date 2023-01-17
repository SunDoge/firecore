from typing import Callable, Dict, Union, List


class Caller:

    def __init__(
        self,
        func: Callable,
        in_rules: Dict[str, str] = {},
        out_rules: Union[Dict[str, str], List[str]] = {},
    ) -> None:
        """
        Some limitations:
        1. input must be kwargs
        2. output must be dict or 1 object or tuple/list
        """

        self._func = func
        self._in_rules = in_rules
        self._out_rules = out_rules

    def __call__(self, **kwargs):
        new_kwargs = kwargs
        if self._in_rules:
            new_kwargs = {
                new_key: kwargs[old_key]
                for new_key, old_key in self._in_rules.items()
            }
        out = self._func(**new_kwargs)

        new_out = out
        if self._out_rules:
            if isinstance(self._out_rules, list):
                if not isinstance(out, tuple):
                    out = (out,)
                new_out = {k: v for k, v in zip(self._out_rules, out)}
            elif isinstance(self._out_rules, dict):
                assert isinstance(out, dict)
                new_out = {
                    new_key: out[old_key]
                    for new_key, old_key in self._out_rules.items()
                }

        return new_out
