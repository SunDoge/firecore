from dataclasses import dataclass
import torch
from torch import Tensor
from typing import (
    List,
    Dict,
    TypeVar,
    Callable,
    Iterator,
    Any,
    Tuple,
    Optional,
    Iterable,
)
from pydantic import BaseModel
from torch.utils.data import DataLoader

T = TypeVar("T")


@dataclass
class Context:
    device: torch.device

    def host_to_device(self, inputs: T) -> T:
        if isinstance(inputs, dict):
            return {k: self.host_to_device(v) for k, v in inputs.items()}
        elif isinstance(inputs, list):
            return [self.host_to_device(x) for x in inputs]
        elif isinstance(inputs, tuple):
            return (self.host_to_device(x) for x in inputs)
        elif isinstance(inputs, Tensor):
            # Must be Tensor, I don't check it
            # non_blocking so we don't have to care about this function performance
            return inputs.to(self.device, non_blocking=True)
        else:
            raise Exception

    def device_to_host(self, inputs: T) -> T:
        pass


class SharedConfig(BaseModel):
    max_epochs: int


DataFunc = Callable[[], Iterable]
ForwardFunc = Callable[[Context, Any], Any]
LossFunc = Callable[[Any, Any], Tuple[Any, Any]]


class Engine:
    def __init__(
        self,
        config: SharedConfig,
        data_func: DataFunc,
        forward_func: ForwardFunc,
        loss_func: LossFunc,
    ) -> None:
        self._config = config
        self._data_func = data_func
        self._forward_func = forward_func
        self._loss_func = loss_func

    def run(self, epoch: int = 1, epoch_length: Optional[int] = None):
        data_source = self._data_func()

        if epoch_length is None:
            for batch_idx, (inputs, targets, metadata) in enumerate(data_source):
                self._one_iteration(batch_idx, inputs, targets, metadata)
        else:
            data_iter = iter(data_source)
            for batch_idx in range(epoch_length):
                inputs, targets, metadata = next(data_source)
                self._one_iteration(batch_idx, inputs, targets, metadata)

    def _one_iteration(self, batch_idx, inputs, targets, metadata):
        ctx = Context(torch.device("cpu"))
        outputs = self._forward_func(ctx, inputs)
        loss, loss_stats = self._loss_func(outputs, targets)
        