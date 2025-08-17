
# Функція, яку тестують
def inc(x):
    return x + 1

import pytest

@pytest.fixture
def mylist():
    return [1, 2, 3]


def test_inc(mylist):    # тут параметр mylist = [1, 2, 3]
    assert inc(5) == 6


