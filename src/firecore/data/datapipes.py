from torch.utils.data import IterDataPipe
from typing import TypeVar, Iterator


T = TypeVar("T")


class Cycler(IterDataPipe[T]):
    def __init__(self, source: IterDataPipe[T], count: int | None = None) -> None:
        super().__init__()
        self.source = source
        self.count = count

        if count is not None and count < 0:
            raise ValueError(f"Expected non-negative count, got {count}")

    def __iter__(self) -> Iterator[T]:
        i = 0
        while self.count is None or i < self.count:
            yield from self.source
            i += 1
