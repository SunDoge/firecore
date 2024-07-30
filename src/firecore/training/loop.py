from pydantic import BaseModel
from typing import List, Dict


class TrainingLoop:
    def __init__(self, data_source) -> None:
        pass


def training_loop(data_source, forward_fn, loss_fn, epoch_length: int):
    for batch_idx in range(epoch_length):
        # metadata is unchanged
        input, target, metadata = next(data_source)
        output = forward_fn(input)
        loss, losses = loss_fn(output, target)

        # Print(losses, batch_idx)
