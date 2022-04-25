DEFAULT_ADDRESS = 1
DEFAULT_BAUDRATE = 9600
DEFAULT_INSTRUMENT_TIMEOUT = .5


class SetUp:
    def __init__(self, archivo):
        self.archivo = archivo

        self.usb = None
        self.csv = None
        self.consulta_por_linea = None
        self.consulta_trifasicas = None
        self.tipo_muestreo = None
        self.periodo_muestreo = None
        self.periodo_registro = None
        self.url = None
        self.address = None
        self.baudrate = None
        self.instrument_timeout = None

        self.cargar_datos(self.leer_archivo())

    def leer_archivo(self):
        with open(self.archivo, 'r') as contenido:
            datos = [self.limpiar_linea(linea) for linea in contenido if self.es_dato(linea)]
            return datos

    @staticmethod
    def es_dato(linea):
        return 'a' <= linea[0] <= 'z' or 'A' <= linea[0] <= 'Z' or '0' <= linea[0] <= '9'

    def limpiar_linea(self, linea):
        data = linea.split()[-1]
        data.replace("\n", "")
        return data

    def cargar_datos(self, datos):
        self.usb = datos[0]
        self.csv = datos[1]
        self.consulta_por_linea = [int(a) for a in datos[2].split(',')]
        self.consulta_trifasicas = [int(a) for a in datos[3].split(',')]
        self.tipo_muestreo = datos[4]
        self.periodo_muestreo = float(datos[5])
        self.periodo_registro = float(datos[6]) * 60.
        self.url = datos[7]
        self.address = DEFAULT_ADDRESS
        self.baudrate = DEFAULT_BAUDRATE
        self.instrument_timeout = DEFAULT_INSTRUMENT_TIMEOUT

    def __str__(self):
        return "\n".join(f"{campo}: {valor}" for campo, valor in self.__dict__.items())
