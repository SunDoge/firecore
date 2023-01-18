
from typing import List, TypedDict, Dict
from .average_meter import AverageMeter
import torch
from torch import Tensor


class MeterCollection:

    def __init__(self, meters: List[AverageMeter]) -> None:
        self._meters = meters

    def update_with_kwargs(self, **kwargs):
        for meter in self._meters:
            meter.update_with_kwargs(**kwargs)

    def sync(self):
        futs = [m.all_reduce_async() for m in self._meters]
        torch.futures.wait_all(futs)

    def summary(self) -> Dict[str, Tensor]:
        result = {}
        for meter in self._meters:
            result[meter.name()] = meter.avg()
        return result
