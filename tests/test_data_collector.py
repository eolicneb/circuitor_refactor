import pytest
from data_collector import DataCollector


def test_data_collector(get_instrument):
    instrument = get_instrument()
    data_collector = DataCollector(instrument, [1, 2], [1, 2, 3, 4], "instant")
    data_collector.muestrear()
    promedios_1 = data_collector.promedios(reset=False)
    assert data_collector.conteo == 1
    assert len(promedios_1) == 10
    data_collector.muestrear()
    assert data_collector.conteo == 2
    promedios_2 = data_collector.promedios()
    assert data_collector.conteo == 0
    assert len(promedios_2) == len(promedios_1)
    assert len(data_collector.encabezados) == 10
