import firecore
import pytest

@pytest.mark.parametrize('foo', ['123', 123, 3.5, True, {}, []])
def test_primitive(foo):
    op = firecore.config.ObjectPool({}, foo=foo)
    assert op.get('foo') == foo
