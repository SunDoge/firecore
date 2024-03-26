from torch import nn


def get_all(model: nn.Module):
    return model.parameters()



class AllParams():
    pass