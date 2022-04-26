import sys
import pytest
from random import randint
from math import fabs


class Instrument:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def read_registers(*args, **kwargs):
        return randint(0, 15), randint(0, 15)


minimalmodbus = type(sys)("minimalmodbus")
minimalmodbus.Instrument = Instrument
sys.modules['minimalmodbus'] = minimalmodbus


@pytest.fixture
def get_instrument():
    def _inner():
        from CircuitorCVM96 import CircuitorCVM96
        return CircuitorCVM96("", 0)
    return _inner


@pytest.fixture
def compare_near():
    def _inner(value_1, value_2, margin):
        return fabs(value_1 - value_2) < fabs(margin)
    return _inner
