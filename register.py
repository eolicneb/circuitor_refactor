import logging
import requests
import threading as thr
from os import environ
from os import path
from time import sleep

from data_collector import DataCollector


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
