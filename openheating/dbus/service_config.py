from .thermometer_client import DBusThermometer
from .switch_client import DBusSwitch

from ..error import HeatingError
from ..config_parser import ConfigParser
from ..switch import Switch
from ..thermometer_center import ThermometerCenter
from ..switch_center import SwitchCenter
from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer
from ..testutils.thermometer import TestThermometer
from ..hardware.switch_gpio import GPIOSwitch
from ..hardware.gpio import create as create_gpio
from ..testutils.switch import TestSwitch

from abc import ABCMeta, abstractmethod


class DBusServiceConfig:
    DAEMON_ADDRESS = 'DAEMON_ADDRESS'
    BUS_NAME = 'BUS_NAME'
    
    def __init__(self, content):
        parser = ConfigParser(symbols=_symbols.copy())
        config = parser.parse(content)

        self.__daemon_address = config.get('DAEMON_ADDRESS')
        self.__bus_name = config.get('BUS_NAME')
        self.__creators = config.get('OBJECTS', {})

        # early sanity
        if self.__daemon_address is None:
            raise HeatingError('"DAEMON_ADDRESS" not specified')
        assert type(self.__daemon_address) is str

        if self.__bus_name is None:
            raise HeatingError('"BUS_NAME" not specified')
        assert type(self.__bus_name) is str

        if self.__creators is None:
            raise HeatingError('"OBJECTS" not specified')
        assert type(self.__creators) is dict
        for path, creator in self.__creators.items():
            assert type(path) is str
            assert isinstance(creator, _Creator)

    def daemon_address(self):
        return self.__daemon_address
    def bus_name(self):
        return self.__bus_name
    def creators(self):
        return self.__creators

class _Creator(metaclass=ABCMeta):
    @abstractmethod
    def create(self, connection):
        pass

class _SwitchCenterCreator(_Creator):
    def __init__(self, switches):
        self.__switches = switches
    def create(self, connection):
        enlightened_switches = {}
        for name, creator in self.__switches.items():
            enlightened_switches[name] = creator.create(connection)
        return SwitchCenter(enlightened_switches)

class _ThermometerCenterCreator(_Creator):
    def __init__(self, thermometers, cache_age=None):
        self.__thermometers = thermometers
        self.__cache_age = cache_age
    def create(self, connection):
        enlightened_thermometers = {}
        for name, creator in self.__thermometers.items():
            enlightened_thermometers[name] = creator.create(connection)
        return ThermometerCenter(thermometers=enlightened_thermometers, cache_age=self.__cache_age)

class _HWMON_I2C_Thermometer(_Creator):
    def __init__(self, bus_number, address):
        self.__bus_number = bus_number
        self.__address = address
    def create(self, connection):
        return HWMON_I2C_Thermometer(bus_number=self.__bus_number, address=self.__address)

class _DBusThermometerCreator(_Creator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create(self, connection):
        return DBusThermometer(connection=connection, name=self.__name, path=self.__path)

class _TestThermometerCreator(_Creator):
    def __init__(self, initial_temperature):
        self.__initial_temperature = initial_temperature
    def create(self, connection):
        return TestThermometer(initial_temperature=self.__initial_temperature)

class _GPIOSwitchCreator(_Creator):
    def __init__(self, number):
        self.__number = number
    def create(self, connection):
        return GPIOSwitch(create_gpio(self.__number))

class _DBusSwitchCreator(_Creator):
    def __init__(self, name, path):
        self.__name = name
        self.__path = path
    def create(self, connection):
        return DBusSwitch(connection=connection, name=self.__name, path=self.__path)

class _TestSwitchCreator(_Creator):
    def __init__(self, initial_state):
        self.__initial_state = initial_state
    def create(self, connection):
        return TestSwitch(initial_state=self.__initial_state)

_symbols = {
    'SwitchCenter': _SwitchCenterCreator,
    'ThermometerCenter': _ThermometerCenterCreator,
    'HWMON_I2C_Thermometer': _HWMON_I2C_Thermometer,
    'DBusThermometer': _DBusThermometerCreator,
    'TestThermometer': _TestThermometerCreator,
    'GPIOSwitch': _GPIOSwitchCreator,
    'DBusSwitch': _DBusSwitchCreator,
    'TestSwitch': _TestSwitchCreator,
    'OPEN': Switch.OPEN,
    'CLOSED': Switch.CLOSED,
}
