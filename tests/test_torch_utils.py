from firecore import torch_utils
import torch

def test_first_param():
    m = torch.nn.Linear(2, 3)
    assert torch_utils.get_first_parameter(m) is m.weight
