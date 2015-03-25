from .object_switch import DBusSwitchObject

from ..testutils.test_thermometer import TestThermometer
from ..testutils.file_thermometer import FileThermometer
from ..testutils.test_switch import TestSwitch
from ..testutils.file_switch import FileSwitch
from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer
from ..hardware.switch_gpio import GPIOSwitch

from ..switch_center import SwitchCenter
from ..thermometer_center import ThermometerCenter

from .client_switch import DBusSwitchClient
from .client_thermometer import DBusThermometerClient

from .object_switch import DBusSwitchObject
from .object_thermometer import DBusThermometerObject
from .object_switch_center import DBusSwitchCenterObject
from .object_thermometer_center import DBusThermometerCenterObject

from abc import ABCMeta, abstractmethod


# ----------------------------------------------------------------
class DBusObjectCreator(metaclass=ABCMeta):
    @abstractmethod
    def create_object(self, connection, path):
        pass

# ----------------------------------------------------------------
class ThermometerObjectConstructor:
    def __init__(self, klass):
        self.__class = klass
    def __call__(self, *args, **kwargs):
        return ThermometerObjectCreator(self.__class, *args, **kwargs)

class ThermometerObjectCreator(DBusObjectCreator):
    def __init__(self, klass, *args, **kwargs):
        self.__class = klass
        self.__args = args
        self.__kwargs = kwargs
    def create_object(self, connection, path):
        return DBusThermometerObject(
            connection=connection,
            path=path,
            thermometer=self.__class(*self.__args, **self.__kwargs))

# ----------------------------------------------------------------
class SwitchObjectConstructor:
    def __init__(self, klass):
        self.__class = klass
    def __call__(self, *args, **kwargs):
        return SwitchObjectCreator(self.__class, *args, **kwargs)

class SwitchObjectCreator(DBusObjectCreator):
    def __init__(self, klass, *args, **kwargs):
        self.__class = klass
        self.__args = args
        self.__kwargs = kwargs
    def create_object(self, connection, path):
        return DBusSwitchObject(
            connection=connection,
            path=path,
            switch=self.__class(*self.__args, **self.__kwargs))

# ----------------------------------------------------------------
class ThermometerCenterObjectCreator(DBusObjectCreator):
    def __init__(self, thermometers):
        self.__thermometers = thermometers

    def create_object(self, connection, path):
        return DBusThermometerCenterObject(
            connection=connection,
            path=path,
            center=ThermometerCenter(self.__thermometers))

# ----------------------------------------------------------------
class SwitchCenterObjectCreator(DBusObjectCreator):
    def __init__(self, switches):
        self.__switches = switches
        
    def create_object(self, connection, path):
        return DBusSwitchCenterObject(
            connection=connection,
            path=path,
            center=SwitchCenter(self.__switches))
