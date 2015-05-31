from .object import DBusObject, DBusObjectCreator
from .types import DBUS_THERMOMETER_CENTER_IFACE_STRING

from ..logic.thermometer_center import ThermometerCenter

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


class ThermometerCenterObjectCreator(DBusObjectCreator):
    def __init__(self, thermometers):
        self.__thermometers = thermometers

    def create_object(self, path):
        return DBusThermometerCenterObject(
            path=path,
            center=ThermometerCenter(self.__thermometers))

