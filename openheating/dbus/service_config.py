from .service_config_native import NativeObjectConstructor
from .object_thermometer import ThermometerObjectConstructor
from .object_switch import SwitchObjectConstructor
from .object_thermometer_center import ThermometerCenterObjectCreator
from .object_switch_center import SwitchCenterObjectCreator
from .object_brain import BrainObjectCreator
from .object_looper import LooperObjectCreator

from .client_switch import DBusSwitchClient
from .client_thermometer import DBusThermometerClient
from .client_switch_center import DBusSwitchCenterClient
from .client_thermometer_center import DBusThermometerCenterClient
from .client_brain import DBusBrainClient
from .client_looper import DBusLooperClient

from .service import DBusService

from ..hardware.switch_gpio import GPIOSwitch
from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer

from ..testutils.test_switch import TestSwitch
from ..testutils.file_switch import FileSwitch
from ..testutils.test_thermometer import TestThermometer
from ..testutils.file_thermometer import FileThermometer

from ..logic.thermometer_center import ThermometerCenterThermometer
from ..logic.switch_center import SwitchCenterSwitch
from ..logic.jf_control import JFControl
from ..logic.lcd import LCD

from ..base.config_parser import ConfigParser


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
    # DBus objects
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

    'BrainObject': BrainObjectCreator,
    'LooperObject': LooperObjectCreator,


    # native objects
    'TestSwitch': NativeObjectConstructor(TestSwitch),
    'FileSwitch': NativeObjectConstructor(FileSwitch),
    'DBusSwitchClient': NativeObjectConstructor(DBusSwitchClient),
    'HWMON_I2C_Thermometer': NativeObjectConstructor(HWMON_I2C_Thermometer),
    'DBusThermometerClient': NativeObjectConstructor(DBusThermometerClient),
    'TestThermometer': NativeObjectConstructor(TestThermometer),
    'FileThermometer': NativeObjectConstructor(FileThermometer),
    'ThermometerCenterThermometer': NativeObjectConstructor(ThermometerCenterThermometer),
    'SwitchCenterSwitch': NativeObjectConstructor(SwitchCenterSwitch),

    'DBusSwitchCenterClient': NativeObjectConstructor(DBusSwitchCenterClient),
    'DBusThermometerCenterClient': NativeObjectConstructor(DBusThermometerCenterClient),

    'DBusBrainClient': NativeObjectConstructor(DBusBrainClient),
    'DBusLooperClient': NativeObjectConstructor(DBusLooperClient),

    'JFControl': NativeObjectConstructor(JFControl),
    'LCD': NativeObjectConstructor(LCD),
}
