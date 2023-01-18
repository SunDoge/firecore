from torch import Tensor


class BaseMeter:

    def update(self, val: Tensor, n: int = 1):
        pass

    def complete(self):
        pass

    def sync(self):
        pass
