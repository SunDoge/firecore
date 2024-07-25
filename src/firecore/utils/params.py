import typing
import torch


class ParamInfo(typing.NamedTuple):
    device: torch.device
    dtype: torch.dtype


def get_param_info(model: torch.nn.Module):
    for p in model.parameters():
        return ParamInfo(p.device, p.dtype)
    raise Exception("failed to find param")
