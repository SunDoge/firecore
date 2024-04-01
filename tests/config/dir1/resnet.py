from firecore.config.lazy import LazyCall, LazyPartial, LazyImport
import torch
# from firecore.factory import ModelFactory
from firecore.params import get_all

# config = LazyCall(dict)(
#     model_factory=LazyCall(ModelFactory)(
#         model=LazyCall(torch.nn.Linear)(10, 20),
#         params=LazyCall(get_all)(),
#         optimizer=LazyCall(torch.optim.SGD)(lr=0.2),
#         lr_scheduler=LazyCall(torch.optim.lr_scheduler.StepLR)(step_size=100),
#     )
# )

config = dict(
    model=LazyCall(torch.nn.Linear)(in_features=10, out_features=20),
    params=LazyPartial(get_all)(),
    optimizer=LazyPartial(torch.optim.SGD)(lr=0.2),
    lr_scheduler=LazyPartial(torch.optim.lr_scheduler.StepLR)(step_size=100),
)
