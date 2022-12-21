from firecore.import_utils import require


def test_require():
    func = require('firecore.import_utils.require')
    assert func is require
