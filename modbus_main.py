#!/usr/bin/env python
# -- coding: utf-8 --
import logging
import requests
import threading as thr
from time import sleep
from os import path, getcwd, environ

from CircuitorCVM96 import CircuitorCVM96

from setup import SetUp
from data_collector import DataCollector
from time_controller import TimeController


archivo_setup = path.join(getcwd(), 'setup.dat')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if "DEBUG" in environ else logging.INFO)


def empezar_thread(funcion, nombre, parametros):
    thr_envio = thr.Thread(group=None, target=funcion,
                           name=nombre, args=parametros)
    thr_envio.start()


def mandar_datos(tiempo, data_collector, url):
    if url is not None:
        try:
            params = {"hora": tiempo}
            params.update(data_collector.promedios_dict())
            requests.get(url, params=params)
            logger.info(f'Los datos se enviaron correctamente a {url}')
        except Exception as e:
            logger.error(f'No se pudo enviar datos a la URL indicada. Error {e}')


def registrar_archivo(tiempo, data_collector: DataCollector, linea=None, intento=0):
    archivo = f"{tiempo.date()}.csv"
    con_encabezado = not path.isfile(archivo) and data_collector.encabezados is not None
    linea = linea if linea else f"{tiempo},{data_collector.promedios_str()}"
    try:
        intento += 1
        with open(archivo, 'a') as f:
            if con_encabezado:
                f.write(f'hora,{data_collector.encabezados}\n')
            f.write(linea + '\n')
        logger.info(f'Se escribio en {archivo}')
    except IOError as error:
        logger.error(f'No se pudo escribir en {archivo} en el intento {intento}. {error}')
        sleep(1)
        registrar_archivo(tiempo, data_collector, linea, intento)


def registrar(tiempo, data_collector, url):
    logger.info(f'Registrando: {tiempo},{data_collector.promedios_str()}')
    empezar_thread(funcion=mandar_datos, nombre='envio',
                   parametros=(tiempo, data_collector, url))
    empezar_thread(funcion=registrar_archivo, nombre='periodo_registro',
                   parametros=(tiempo, data_collector))


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
            collector.promedios()
            registrar(ahora, collector, setup.url)


if __name__ == "__main__":
    main()
