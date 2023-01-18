from .base import BaseMeter
import torch.distributed as dist
import torch
import numpy as np
from torch import Tensor
from typing import Dict


class AverageMeter(BaseMeter):

    def __init__(self, name: str, in_rules: Dict[str, str] = {}, fmt: str = ':f', device=torch.device('cpu')) -> None:
        super().__init__()

        self._name = name
        self._fmt = fmt

        self._val = torch.tensor(0., dtype=torch.float, device=device)
        self._sum = torch.tensor(0., dtype=torch.float, device=device)
        self._count = torch.tensor(0, dtype=torch.float, device=device)
        self._in_rules = in_rules

        self.device = device

    @torch.inference_mode()
    def update(self, *, val: Tensor, n: int = 1):
        self._val.copy_(val)
        self._sum.add_(val, alpha=n)
        self._count.add_(n)

    def avg(self) -> Tensor:
        """
        Average value
        """
        return self._sum / self._count

    def val(self) -> Tensor:
        """
        Current value
        """
        return self._val

    def name(self) -> str:
        return self._name

    def sync(self):
        fut = self.all_reduce_async()
        fut.wait()

    def all_reduce_async(self) -> torch.futures.Future:
        fut_count = dist.all_reduce(
            self._count, op=dist.ReduceOp.SUM, async_op=True)
        fut_sum = dist.all_reduce(
            self._sum, op=dist.ReduceOp.SUM, async_op=True)
        return torch.futures.collect_all([fut_count, fut_sum])
