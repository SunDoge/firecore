from firecore.caller import Caller


def criterion(*, pred, target):
    return {'loss': 1}


def model(*, image, text, **kwargs):
    return {'pred_image': 1, 'pred_text': 2}


def test_empty():
    caller = Caller(criterion)
    out = caller(pred=1, target=2)
    assert out['loss'] == 1


def test_in_rules():
    caller = Caller(criterion, in_rules=dict(pred='output', target='label'))
    out = caller(output=1, label=2)
    assert out['loss'] == 1


def test_out_rules_list():
    caller = Caller(criterion, in_rules=dict(
        pred='output', target='label'), out_rules={'loss1': 'loss'})
    out = caller(output=1, label=2)
    assert out['loss1'] == 1


def test_out_rules_dict():
    caller = Caller(model, in_rules=dict(
        image='img', text='label'), out_rules=dict(image='pred_image', text='pred_text'))
    out = caller(img=1, label=2)
    assert out['image'] == 1
    assert out['text'] == 2
