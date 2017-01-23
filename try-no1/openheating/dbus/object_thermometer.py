from .object import DBusObject, DBusObjectCreator
from .types import DBUS_THERMOMETER_IFACE_STRING

from ..logic.thermometer import Thermometer

import dbus.service


class DBusThermometerObject(DBusObject):
    '''Adapt a Thermometer into a DBus object at object_path'''

    def __init__(self, path, thermometer):
        self.__thermometer = thermometer
        DBusObject.__init__(self, path=path)

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_IFACE_STRING, out_signature = 'd')
    def temperature(self):
        return self.object_call(self.__thermometer.temperature)


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
    def create_object(self, path):
        return DBusThermometerObject(
            path=path,
            thermometer=self.__class(*self.__args, **self.__kwargs))

