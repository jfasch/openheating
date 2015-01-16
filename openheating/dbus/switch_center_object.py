from .object import DBusObject
from .types import exception_local_to_dbus, DBUS_SWITCH_CENTER_IFACE_STRING

from ..switch import Switch
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
            if value:
                switch_state = Switch.CLOSED
            else:
                switch_state = Switch.OPEN
            self.__center.set_state(name, switch_state)
        except HeatingError as e:
            raise exception_local_to_dbus(e)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_CENTER_IFACE_STRING, in_signature='s', out_signature = 'b')
    def get_state(self, name):
        try:
            value = self.__center.get_state(name)
            if value == Switch.OPEN:
                return False
            elif value == Switch.CLOSED:
                return True
            else:
                assert False, value
        except HeatingError as e:
            raise exception_local_to_dbus(e)
