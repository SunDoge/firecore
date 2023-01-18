from firecore.torch.metrics.accuracy import Accuracy
from firecore.torch.metrics.batch_size import BatchSize
from firecore.caller import Caller
import torch


def test_two():

    data = dict(
        pred=torch.rand(10, 20),
        target=torch.zeros(10, dtype=torch.long),
    )

    acc = Caller(Accuracy([1, 5]))
    batch_size = Caller(BatchSize(), in_rules={'data': 'pred'})

    out = {}
    out.update(acc(**data))
    out.update(batch_size(**data))
    print(out)

    assert out['batch_size'] == 10
    assert out['acc1'] <= 100.0
    assert out['acc5'] <= 100.0


# test_two()
