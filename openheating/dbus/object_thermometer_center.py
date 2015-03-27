from .object import DBusObject
from .types import DBUS_THERMOMETER_CENTER_IFACE_STRING

import dbus
import dbus.service


class DBusThermometerCenterObject(DBusObject):
    '''Adapt a ThermometerCenter into a DBus object'''

    def __init__(self, path, center):
        self.__center = center
        DBusObject.__init__(self, path=path)

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_CENTER_IFACE_STRING, out_signature='as')
    def all_names(self):
        return self.object_call(self.__center.all_names)

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_CENTER_IFACE_STRING, in_signature='s', out_signature='d')
    def temperature(self, name):
        return self.object_call(self.__center.temperature, name)
