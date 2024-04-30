from torch import nn, Tensor


class BaseMeter(nn.Module):
    def reset(self):
        pass
