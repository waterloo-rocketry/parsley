import pytest

FLOAT_TOLERANCE = 0.01

def approx(value):
    return pytest.approx(value, FLOAT_TOLERANCE)
