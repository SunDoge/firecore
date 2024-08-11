import numpy as np
from pydantic import BaseModel


class AverageMeter(BaseModel):
    val: float = 0.0
    sum: float = 0
    count: int = 0

    def update(self, val: float, n: int = 1):
        self.val = val
        self.sum += val * n
        self.count += n

    @property
    def avg(self):
        return self.sum / self.count
