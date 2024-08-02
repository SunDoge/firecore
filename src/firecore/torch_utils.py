import typing
import torch


def get_first_parameter(model: torch.nn.Module):
    for p in model.parameters():
        return p
    raise Exception("paramter not found")
