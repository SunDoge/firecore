from firecore.config.lazy import LazyCall, LazyPartial, LazyImport
from firecore.config import _types
from utils import Net
from firecore.params import get_all
import torch
import torch.optim
import torch.optim.lr_scheduler
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


trans = LazyCall(transforms.Compose)(
    transforms=[
        LazyCall(transforms.ToTensor)(),
        LazyCall(transforms.Normalize)(mean=(0.1307,), std=(0.3081,)),
    ]
)

config = _types.Config(
    strategy=_types.Strategy(max_epochs=14),
    model=LazyCall(Net)(),
    params=LazyPartial(get_all)(),
    optimizer=LazyPartial(torch.optim.Adadelta)(lr=1.0),
    lr_scheduler=LazyPartial(torch.optim.lr_scheduler.StepLR)(step_size=1, gamma=0.7),
    train=_types.Train(
        loader=LazyCall(DataLoader)(
            batch_size=64,
            num_workers=1,
            pin_memory=True,
            shuffle=True,
            dataset=LazyCall(datasets.MNIST)(
                root="/tmp",
                train=True,
                download=True,
                transform=trans,
            ),
        )
    ),
    val=_types.Val(
        loader=LazyCall(DataLoader)(
            batch_size=1000,
            num_workers=1,
            pin_memory=True,
            shuffle=False,
            dataset=LazyCall(datasets.MNIST)(root="/tmp", train=False, transform=trans),
        )
    ),
)
