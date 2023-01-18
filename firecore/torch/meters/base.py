from torch import Tensor
from typing import Dict


class BaseMeter:
    def __init__(self, in_rules: Dict[str, str] = {}) -> None:
        self._in_rules = in_rules

    def update_with_kwargs(self, **kwargs):
        assert self._in_rules
        new_kwargs = kwargs
        if self._in_rules:
            new_kwargs = {
                new_key: kwargs[old_key]
                for new_key, old_key in self._in_rules.items()
            }

        self.update(**new_kwargs)

    def update(self, *, val: Tensor, n: int = 1):
        pass

    def complete(self):
        pass

    def sync(self):
        pass
