#!/usr/bin/env python
# -- coding: utf-8 --
import logging
from os import path, getcwd, environ

from CircuitorCVM96 import CircuitorCVM96

from setup import SetUp
from data_collector import DataCollector
from time_controller import TimeController
from register import registrar


archivo_setup = path.join(getcwd(), 'setup.dat')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if "DEBUG" in environ else logging.INFO)


def main():
    setup = SetUp(archivo_setup)
    logger.info(setup)

    instrumento = CircuitorCVM96(port_name=setup.usb,
                                 slave_address=1,
                                 baud_rate=setup.baudrate,
                                 timeout=setup.instrument_timeout)

    collector = DataCollector(instrumento=instrumento,
                              consulta_por_linea=setup.consulta_por_linea,
                              consulta_trifasica=setup.consulta_trifasicas,
                              tipo_muestreo=setup.tipo_muestreo)

    time_controller = TimeController(setup.periodo_muestreo, setup.periodo_registro)

    for ahora in time_controller:
        if time_controller.es_hora_de_muestreo():
            print(ahora)
            collector.muestrear()

        if time_controller.es_hora_de_registro():
            collector.calcular_promedios()
            registrar(ahora, collector, setup.url)


if __name__ == "__main__":
    main()
