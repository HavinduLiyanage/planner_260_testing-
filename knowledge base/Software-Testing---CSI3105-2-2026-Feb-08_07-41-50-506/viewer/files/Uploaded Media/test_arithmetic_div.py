import pytest
from logic.simple_arithmetic import SimpleArithmetic

# Fixture to create an instance of SimpleArithmetic before each test
@pytest.fixture
def arithmetic():
    return SimpleArithmetic()

def test_div_int_pass(arithmetic):
    assert arithmetic.div_int_two_no(27, 3) == 9, "error in div_int_two_no()"
    assert arithmetic.div_int_two_no(2, 8) == 0, "error in div_int_two_no()"

def test_div_int_fail(arithmetic):
    assert arithmetic.div_int_two_no(27, 3) != 3, "error in div_int_two_no()"

def test_div_int_by_zero(arithmetic):
    with pytest.raises(ValueError):
        arithmetic.div_int_two_no(5, 0)

def test_div_real_pass(arithmetic):
    assert pytest.approx(arithmetic.div_real_two_no(2, 3), rel=1e-6) == 0.666666, "error in div_real_two_no()"
    assert pytest.approx(arithmetic.div_real_two_no(2, 9), rel=1e-6) == 0.222222, "error in div_real_two_no()"

def test_div_real_by_zero(arithmetic):
    with pytest.raises(ValueError):
        arithmetic.div_real_two_no(3, 0)
