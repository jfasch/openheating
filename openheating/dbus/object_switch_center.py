from .object import DBusObject
from .types import exception_local_to_dbus, DBUS_SWITCH_CENTER_IFACE_STRING

from ..error import HeatingError

import dbus
import dbus.service


class DBusSwitchCenterObject(DBusObject):
    '''Adapt a SwitchCenter into a DBus object at object_path'''

    def __init__(self, connection, path, center):
        self.__center = center
        DBusObject.__init__(self, connection=connection, path=path)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_CENTER_IFACE_STRING, out_signature='as')
    def all_names(self):
        return self.__center.all_names()

    @dbus.service.method(dbus_interface=DBUS_SWITCH_CENTER_IFACE_STRING, in_signature = 'sb')
    def set_state(self, name, value):
        try:
            # have to convert from "dbus.Boolean" which slips through
            self.__center.set_state(name, value and True or False)
        except HeatingError as e:
            raise exception_local_to_dbus(e)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_CENTER_IFACE_STRING, in_signature='s', out_signature = 'b')
    def get_state(self, name):
        try:
            return self.__center.get_state(name)
        except HeatingError as e:
            raise exception_local_to_dbus(e)
