from firecore.torch.meters.meter_collection import MeterCollection
from firecore.torch.meters.average_meter import AverageMeter
import torch
import copy
from firecore.torch.testing import init_single_gloo_process_group


def test_meter_collection():

    mc = MeterCollection(
        [
            AverageMeter('acc1', in_rules={'val': 'acc1', 'n': 'batch_size'}),
            AverageMeter('acc5', in_rules={'val': 'acc5', 'n': 'batch_size'}),
            AverageMeter('loss', in_rules={'val': 'loss', 'n': 'batch_size'}),
        ]
    )

    data1 = dict(
        acc1=torch.tensor(20.),
        acc5=torch.tensor(30.),
        loss=torch.tensor(0.5),
        batch_size=10,
        asdf='fdsa',
    )
    data2 = copy.deepcopy(data1)
    data2['batch_size'] = 5

    mc.update_with_kwargs(**data1)
    print(mc.summary())
    mc.update_with_kwargs(**data2)
    print(mc.summary())

test_meter_collection()
