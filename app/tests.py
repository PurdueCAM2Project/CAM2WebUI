import pytest

# Simple function and test to verify Travis functionality
def func(a):
    return a + 1

def test_func():
    assert(func(3) == 4)
    with pytest.raises(TypeError):
        func('string')
