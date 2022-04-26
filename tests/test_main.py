import pytest
from time import time, sleep
from io import StringIO
from collections import namedtuple

from time_controller import Time
from data_collector import DataCollector, CommaList
import modbus_main


class DataNotCollector(DataCollector):
    _encabezados = CommaList(["campo_1", "campo_2"])
    ultimos_promedios = [1.0, 2.0]

    def __init__(self):
        pass

    @property
    def encabezados(self):
        return self._encabezados


class PersistentIO(StringIO):
    content = ""

    def close(self):
        self.content = self.getvalue()
        super().close()


@pytest.fixture
def mock_mandar_datos(mocker):
    mock = mocker.patch('modbus_main.requests.get')
    return mock


@pytest.fixture
def mock_registrar_archivo(mocker):
    mock_file = PersistentIO()
    mock_open = mocker.patch('modbus_main.open', return_value=mock_file)
    Mock = namedtuple('Mock', "function file")
    return Mock(mock_open, mock_file)


def test_registrar(mock_registrar_archivo, mock_mandar_datos):
    collector = DataNotCollector()
    modbus_main.registrar(Time(time()), collector, "http.com")
    sleep(.1)
    assert mock_mandar_datos.called
    assert all(campo in mock_mandar_datos.call_args_list[0].kwargs['params']
               for campo in collector.encabezados)
    assert mock_registrar_archivo.function.called
    while not mock_registrar_archivo.file.closed:
        sleep(.01)
    file_content = [line.split(",") for line
                    in mock_registrar_archivo.file.content.split("\n") if line]
    assert len(file_content) > 1
    assert all(len(file_content[0]) == len(line) for line in file_content[1:])
