import torch
from torch import nn, Tensor
from .base import BaseMeter


class AverageMeter(BaseMeter):
    val: Tensor
    sum: Tensor
    count: Tensor
    avg: Tensor

    def __init__(self):
        super().__init__()
        self.register_buffer("val", torch.tensor(0.0))
        self.register_buffer("sum")

    def reset(self):
        return super().reset()
