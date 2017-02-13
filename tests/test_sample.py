"""
This file is to verify pytest and Travis functionality.
"""

def test_one():
    """Perform a trivial assert."""
    assert True

def func(num):
    """Increment a number by one."""
    return num+1

def test_two():
    """Test func"""
    assert func(3) == 4
