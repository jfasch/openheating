from .object import DBusObject
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
