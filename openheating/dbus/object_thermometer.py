from .object import DBusObject
from .types import exception_local_to_dbus, DBUS_THERMOMETER_IFACE_STRING

from ..thermometer import Thermometer
from ..error import HeatingError

import dbus.service


class DBusThermometerObject(DBusObject):
    '''Adapt a Thermometer into a DBus object at object_path'''

    def __init__(self, path, thermometer):
        self.__thermometer = thermometer
        DBusObject.__init__(self, path=path)

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_IFACE_STRING, out_signature = 'd')
    def temperature(self):
        try:
            return self.__thermometer.temperature()
        except HeatingError as e:
            raise exception_local_to_dbus(e)
