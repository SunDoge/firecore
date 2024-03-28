import torch
from typing import Iterable, Dict


# class ModelFactory:
#     model: torch.nn.Module
#     params: Iterable[torch.Tensor] | Iterable[Dict[str, torch.Tensor]]
#     optimizer: torch.optim.Optimizer
#     lr_scheduler: torch.optim.lr_scheduler._LRScheduler

#     def __init__(
#         self,
#         model: Node,
#         params: Node,
#         optimizer: Node,
#         lr_scheduler: Node,
#     ):
#         self.model = model.instantiate(recursive=True)
#         self.params = params.target(self.model, *params.args, **params.kwargs)
#         self.optimizer = optimizer.target(
#             self.params, *optimizer.args, **optimizer.kwargs
#         )
#         self.lr_scheduler = lr_scheduler.target(
#             self.optimizer, *lr_scheduler.args, **lr_scheduler.kwargs
#         )
