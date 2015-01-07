from .types import exception_local_to_dbus, DBUS_SWITCH_CENTER_IFACE_STRING

from ..thermometer_center import ThermometerCenter
from ..error import HeatingError

import dbus
import dbus.service


class DBusThermometerCenterObject(dbus.service.Object):
    '''Adapt a ThermometerCenter into a DBus object at object_path'''

    def __init__(self, connection, object_path, center):
        self.__center = center
        dbus.service.Object.__init__(self, conn=connection, object_path=object_path)

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_CENTER_IFACE_STRING, out_signature='as')
    def all_names(self):
        return self.__center.all_names()

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_CENTER_IFACE_STRING, in_signature='s', out_signature='d')
    def temperature(self, name):
        try:
            return self.__center.temperature(name)
        except HeatingError as e:
            raise exception_local_to_dbus(e)
