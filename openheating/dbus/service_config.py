from .native_creator import NativeObjectCreator
from ..testutils.test_switch import TestSwitch
from ..testutils.file_switch import FileSwitch
from ..hardware.switch_gpio import GPIOSwitch
from .switch_client import DBusSwitchClient

from .object_creator import ThermometerObjectConstructor
from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer
from .thermometer_client import DBusThermometerClient
from ..testutils.test_thermometer import TestThermometer
from ..testutils.file_thermometer import FileThermometer

from .object_creator import SwitchObjectConstructor
from ..hardware.switch_gpio import GPIOSwitch
from .switch_client import DBusSwitchClient
from ..testutils.test_switch import TestSwitch
from ..testutils.file_switch import FileSwitch

from .service import DBusService

from .object_creator import SwitchCenterObjectCreator
from .object_creator import ThermometerCenterObjectCreator

from ..config_parser import ConfigParser


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
    'TestSwitch': NativeObjectCreator(TestSwitch),
    'FileSwitch': NativeObjectCreator(FileSwitch),
    'DBusSwitchClient': NativeObjectCreator(DBusSwitchClient),
    'HWMON_I2C_Thermometer': NativeObjectCreator(HWMON_I2C_Thermometer),
    'DBusThermometerClient': NativeObjectCreator(DBusThermometerClient),
    'TestThermometer': NativeObjectCreator(TestThermometer),
    'FileThermometer': NativeObjectCreator(FileThermometer),

    'SwitchCenterObject': SwitchCenterObjectCreator,
    'ThermometerCenterObject': ThermometerCenterObjectCreator,

    'HWMON_I2C_ThermometerObject': ThermometerObjectConstructor(HWMON_I2C_Thermometer),
    'DBusThermometerClientObject': ThermometerObjectConstructor(DBusThermometerClient),
    'TestThermometerObject': ThermometerObjectConstructor(TestThermometer),
    'FileThermometerObject': ThermometerObjectConstructor(FileThermometer),

    'GPIOSwitchObject': SwitchObjectConstructor(GPIOSwitch),
    'DBusSwitchClientObject': SwitchObjectConstructor(DBusSwitchClient),
    'TestSwitchObject': SwitchObjectConstructor(TestSwitch),
    'FileSwitchObject': SwitchObjectConstructor(FileSwitch),
}
