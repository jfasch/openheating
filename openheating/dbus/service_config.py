from .thermometer_client import DBusThermometer
from .switch_client import DBusSwitch

from .service import DBusService
from .service import SwitchCenterCreator
from .service import ThermometerCenterCreator
from .service import HWMON_I2C_ThermometerCreator
from .service import DBusThermometerCreator
from .service import TestThermometerCreator
from .service import FileThermometerCreator
from .service import GPIOSwitchCreator
from .service import DBusSwitchCreator
from .service import TestSwitchCreator
from .service import FileSwitchCreator

from ..error import HeatingError
from ..config_parser import ConfigParser
from ..switch import Switch
from ..thermometer_center import ThermometerCenter
from ..switch_center import SwitchCenter
from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer
from ..hardware.switch_gpio import GPIOSwitch
from ..hardware.gpio import create as create_gpio

from abc import ABCMeta, abstractmethod


class DBusServicesConfig:
    def __init__(self, content):
        self.__services = []

        parser = ConfigParser(symbols=_symbols.copy())
        config = parser.parse(content)

        daemon_address = config.get('DAEMON_ADDRESS')
        service_specs = config.get('SERVICES')

        if daemon_address is None:
            raise HeatingError('"DAEMON_ADDRESS" not specified')
        if type(daemon_address) is not str:
            raise HeatingError('"DAEMON_ADDRESS" must have string type (was %s)' % str(type(daemon_address)))
        if service_specs is None:
            raise HeatingError('"SERVICES" not specified')
        if type(service_specs) is not dict:
            raise HeatingError('"SERVICES" must have dictionary type (was %s)' % str(type(service_specs)))
     
        for service_name, object_creators in service_specs.items():
            self.__services.append(
                DBusService(daemon_address=daemon_address, 
                            name=service_name, 
                            object_creators=object_creators))

    def services(self):
        return self.__services

_symbols = {
    'SwitchCenter': SwitchCenterCreator,
    'ThermometerCenter': ThermometerCenterCreator,
    'HWMON_I2C_Thermometer': HWMON_I2C_ThermometerCreator,
    'DBusThermometer': DBusThermometerCreator,
    'TestThermometer': TestThermometerCreator,
    'FileThermometer': FileThermometerCreator,
    'GPIOSwitch': GPIOSwitchCreator,
    'DBusSwitch': DBusSwitchCreator,
    'TestSwitch': TestSwitchCreator,
    'FileSwitch': FileSwitchCreator,
}
