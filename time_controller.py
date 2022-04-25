from time import time, asctime, localtime
from datetime import date


class Time(float):
    def __str__(self):
        return asctime(localtime(self))

    def date(self):
        date_tiempo = date.fromtimestamp(self)
        return date_tiempo.strftime('%Y-%m-%d')


class TimeController:
    def __init__(self, periodo_muestreo: [int, float], periodo_registro: [int, float]):
        self.muestreo = periodo_muestreo
        self.registro = periodo_registro
        self.nuevo_muestreo = 0.0
        self.nuevo_registro = 0.0

        self.ahora = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.ahora = time()
        return Time(self.ahora)

    def es_hora_de_muestreo(self):
        if self.ahora < self.nuevo_muestreo:
            return False
        hora_este_muestreo = self.nuevo_muestreo if self.ahora < self.nuevo_muestreo + self.muestreo else self.ahora
        self.nuevo_muestreo = hora_este_muestreo + self.muestreo
        return True

    def es_hora_de_registro(self):
        if self.ahora < self.nuevo_registro:
            return False
        hora_este_registro = self.nuevo_registro if self.ahora < self.nuevo_registro + self.registro else self.ahora
        self.nuevo_registro = hora_este_registro + self.registro
        return True
