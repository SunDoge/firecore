from firecore.data.datapipes import Cycler


def test_cycler():
    dp = Cycler(range(10), count=1)
    assert list(dp) == list(range(10))

    dp = Cycler(range(10), count=2)
    assert list(dp) == list(range(10)) + list(range(10))

    dp = Cycler(range(10))
    for a, b in zip(range(20), dp):
        assert a % 10 == b
