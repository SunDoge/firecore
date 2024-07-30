local x = import './local.jsonnet';

{
  model: { _type: 'call:utils.Net' },
  params: {
    _type: 'call:firecore.params.get_all',
    model: 'ref:model',
  },
  optimizer: {
    _type: 'call:torch.optim.Adadelta',
    params: 'ref:params',
    lr: 1,
  },
  lr_scheduler: {
    _type: 'call:torch.optim.lr_scheduler.StepLR',
    step_size: 1,
    gamma: 0.7,
  },
  x: x,
}
