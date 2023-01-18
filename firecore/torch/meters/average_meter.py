from .base import BaseMeter
import torch.distributed as dist
import torch
import numpy as np
from torch import Tensor


class AverageMeter(BaseMeter):

    def __init__(self, name: str, fmt: str = ':f', device=torch.device('cpu')) -> None:
        super().__init__()

        self._name = name
        self._fmt = fmt

        self._val = torch.tensor(0., dtype=torch.float, device=device)
        self._sum = torch.tensor(0., dtype=torch.float, device=device)
        self._count = torch.tensor(0, dtype=torch.float, device=device)

        self.device = device

    @torch.inference_mode()
    def update(self, val: Tensor, n: int = 1):
        self._val.copy_(val)
        self._sum.add_(val, alpha=n)
        self._count.add_(n)

    def avg(self) -> Tensor:
        return self._sum / self._count

    def val(self) -> Tensor:
        return self._val

    def sync(self):
        promise_count = dist.all_reduce(
            self._count, op=dist.ReduceOp.SUM, async_op=True)
        promise_sum = dist.all_reduce(
            self._sum, op=dist.ReduceOp.SUM, async_op=True)
        promise_count.wait()
        promise_sum.wait()
