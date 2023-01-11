from firecore.resolver import resolve
from dataclasses import dataclass


def test_resolve_int():
    n = 100
    res = resolve(n)
    assert res == n


def test_resolve_list():
    x = [1, 2, 3]
    res = resolve(x)
    assert res == x


def test_resolve_dict():
    x = {"a": 1, "b": 2}
    res = resolve(x)
    assert res == x


@dataclass
class A:
    foo: str
    bar: int = 1


@dataclass
class B:
    a: A
    foo: str
    bar: int = 1


def test_resolve_object():
    a: A = resolve(dict(
        _call="tests.test_resolver.A",
        _0="test",
        bar=100,
    ))

    assert isinstance(a, A)
    assert a.foo == 'test'
    assert a.bar == 100


def test_resolve_nested():
    b: B = resolve(dict(
        _call="tests.test_resolver.B",
        _0=dict(
            _call="tests.test_resolver.A",
            _0="test",
        ),
        _1="100",
        bar=100,
    ))
    assert b.a.foo == 'test'
    assert b.a.bar == 1
    assert b.foo == "100"
    assert b.bar == 100
