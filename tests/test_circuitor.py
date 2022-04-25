import pytest


def test_circuitor(get_instrument):
    instrument = get_instrument("", 0)
    assert instrument.get_Voltage_Phase()
