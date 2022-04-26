from CircuitorCVM96 import CircuitorCVM96
from functools import cached_property


class CommaList(list):
    def __str__(self):
        return ",".join(self)


class DataCollector:
    def __init__(self, instrumento: CircuitorCVM96, consulta_por_linea: list, consulta_trifasica: list,
                 tipo_muestreo: str):
        self.instrumento = instrumento
        self.por_linea = consulta_por_linea
        self.trifasica = consulta_trifasica
        self.tipo_muestreo = tipo_muestreo

        self.datos = []
        self.ultimos_promedios = []

    @property
    def conteo(self):
        return len(self.datos)

    def reset_registro(self):
        self.datos = []

    @cached_property
    def encabezados(self):
        encabezados = [f"{self.instrumento.TitulosDeFuncionesPorLinea[a]} L{n}"
                       for n in [1, 2, 3] for a in self.por_linea]
        encabezados += [self.instrumento.TitulosDeFuncionesTrifasicas[b] for b in self.trifasica]
        return CommaList(encabezados)

    def muestrear(self):
        datos_por_linea = [self.instrumento.FuncionesPorLinea[consulta](L=n, cual=self.tipo_muestreo)
                           for n in [1, 2, 3] for consulta in self.por_linea]
        datos_trifasica = [self.instrumento.FuncionesTrifasicas[consulta](cual=self.tipo_muestreo)
                           for consulta in self.trifasica]
        self.datos.append(datos_por_linea + datos_trifasica)

    def calcular_promedios(self, reset=True):
        promedios = [sum(column) / self.conteo for column in zip(*self.datos)]
        if reset:
            self.reset_registro()
        self.ultimos_promedios = promedios

    def promedios_dict(self):
        return {field: value for field, value in zip(self.encabezados, self.ultimos_promedios)}

    def promedios_str(self):
        return ",".join(str(value) for value in self.ultimos_promedios)
