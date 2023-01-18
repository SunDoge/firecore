from typing import Sequence, List
from torch import Tensor
from .base import BaseMetric


class Accuracy(BaseMetric):

    def __init__(self, topk: List[int]) -> None:
        self._topk = topk

    def __call__(self, *, pred: Tensor, target: Tensor, **kwargs) -> List[Tensor]:
        res = accuracy(pred, target, self._topk)
        assert len(res) == len(self._topk)
        out = {'acc{}'.format(k): v for k, v in zip(self._topk, res)}
        return out


def accuracy(output: Tensor, target: Tensor, topk: List[int]) -> List[Tensor]:
    """Computes the accuracy over the k top predictions for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred: Tensor = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res


if __name__ == '__main__':
    import torch
    jit_accuracy = torch.jit.script_if_tracing(accuracy)
    x = torch.rand(2, 3)
    y = torch.zeros(2, dtype=torch.long)
    res = jit_accuracy(x, y, [1])
    print(res)
