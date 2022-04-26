import pytest
from time_controller import TimeController
from time import time, sleep


def test_clean_run(compare_near):
    periodo_muestreo = .3
    periodo_registro = .7
    margen = min(periodo_registro, periodo_muestreo) / 10
    paro = max(periodo_registro, periodo_muestreo) + 1.1
    controller = TimeController(periodo_muestreo, periodo_registro)
    inicio = time()
    muestreos, registros = 0, 0
    for ahora in controller:
        if controller.es_hora_de_muestreo():
            assert compare_near(ahora, inicio + periodo_muestreo * muestreos, margen)
            muestreos += 1
        if controller.es_hora_de_registro():
            assert compare_near(ahora, inicio + periodo_registro * registros, margen)
            registros += 1
        if muestreos > 1 and registros > 1:
            break
        if ahora > inicio + paro:
            raise Exception("No anduvo")
        sleep(margen/2)
