import pytest
from logic.simple_arithmetic import SimpleArithmetic

# Fixture to create an instance of SimpleArithmetic before each test
@pytest.fixture
def arithmetic():
    return SimpleArithmetic()

def test_add_pass(arithmetic):
    assert arithmetic.add_two_no(1, 3) == 4, "error in add()"
    assert arithmetic.add_two_no(-1, -2) == -3, "error in add()"
    assert arithmetic.add_two_no(9, 0) == 9, "error in add()"

def test_add_fail(arithmetic):
    assert arithmetic.add_two_no(1, 2) != 0, "error in add()"

def test_sub_pass(arithmetic):
    assert arithmetic.sub_two_no(2, 1) == 1, "error in sub()"
    assert arithmetic.sub_two_no(-2, -1) == -1, "error in sub()"
    assert arithmetic.sub_two_no(2, 2) == 0, "error in sub()"

def test_sub_fail(arithmetic):
    assert arithmetic.sub_two_no(2, 1) != 0, "error in sub()"
