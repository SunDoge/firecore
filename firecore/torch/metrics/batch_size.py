from torch import Tensor
from .base import BaseMetric


class BatchSize(BaseMetric):

    def __init__(self, dim: int = 0) -> None:
        self._dim = dim

    def __call__(self, *, data: Tensor, **kwargs):
        batch_size: int = data.size(self._dim)
        return {'batch_size': batch_size}
