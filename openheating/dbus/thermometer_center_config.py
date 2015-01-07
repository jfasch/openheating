from .service_config import DBusServiceConfig
from .thermometer_client import DBusThermometer

from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer
from ..testutils.thermometer import TestThermometer

from abc import ABCMeta, abstractmethod


class ThermometerCenterConfig(DBusServiceConfig):
    PATH = 'PATH'
    CACHE_AGE = 'CACHE_AGE'
    THERMOMETERS = 'THERMOMETERS'
    
    def __init__(self, content):
        DBusServiceConfig.__init__(
            self,
            symbols={
                'HWMON_I2C_Thermometer': _HWMON_I2C_ThermometerCreator,
                'TestThermometer': _TestThermometerCreator,
                'DBusThermometer': _DBusThermometerCreator,
                },
            content=content)

        self.__path = self.config()[self.PATH]
        self.__cache_age = self.config().get(self.CACHE_AGE)
        self.__thermometers = self.config()[self.THERMOMETERS]

        assert self.__cache_age is None or type(self.__cache_age) is int

        assert type(self.__path) is str
        for name, creator in self.__thermometers:
            assert type(name) is str
            assert isinstance(creator, _Creator)

    def path(self):
        return self.__path
    def cache_age(self):
        return self.__cache_age
    def iter_thermometers(self):
        return self.__thermometers

class _Creator(metaclass=ABCMeta):
    @abstractmethod
    def create(self, connection_proxy):
        pass
    
class _HWMON_I2C_ThermometerCreator(_Creator):
    def __init__(self, bus_number, address):
        self.__bus_number = bus_number
        self.__address = address
    def create(self, connection_proxy):
        return HWMON_I2C_Thermometer(bus_number=self.__bus_number, address=self.__address)

class _TestThermometerCreator(_Creator):
    def __init__(self, initial_temperature):
        self.__initial_temperature = initial_temperature
    def create(self, connection_proxy):
        return TestThermometer(initial_temperature=self.__initial_temperature)

class _DBusThermometerCreator(_Creator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create(self, connection_proxy):
        return DBusThermometer(connection_proxy=connection_proxy, name=self.__name, path=self.__path)
