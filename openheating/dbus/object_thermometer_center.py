from .object import DBusObject
from .types import exception_local_to_dbus, DBUS_THERMOMETER_CENTER_IFACE_STRING

from ..error import HeatingError

import dbus
import dbus.service


class DBusThermometerCenterObject(DBusObject):
    '''Adapt a ThermometerCenter into a DBus object at object_path'''

    def __init__(self, connection, path, center):
        self.__center = center
        DBusObject.__init__(self, connection=connection, path=path)

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_CENTER_IFACE_STRING, out_signature='as')
    def all_names(self):
        return self.__center.all_names()

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_CENTER_IFACE_STRING, in_signature='s', out_signature='d')
    def temperature(self, name):
        try:
            return self.__center.temperature(name)
        except HeatingError as e:
            raise exception_local_to_dbus(e)
