from .object import DBusObject
from .types import exception_local_to_dbus, DBUS_SWITCH_IFACE_STRING

from ..error import HeatingError

import dbus.service


class DBusSwitchObject(DBusObject):
    '''Adapt a Switch into a DBus object at object_path'''

    def __init__(self, path, switch):
        DBusObject.__init__(self, path=path)
        self.__switch = switch

    @dbus.service.method(dbus_interface=DBUS_SWITCH_IFACE_STRING, in_signature = 'b')
    def set_state(self, value):
        try:
            # have to convert from "dbus.Boolean" which slips through
            self.__switch.set_state(value and True or False)
        except HeatingError as e:
            raise exception_local_to_dbus(e)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_IFACE_STRING, out_signature = 'b')
    def get_state(self):
        try:
            return self.__switch.get_state()
        except HeatingError as e:
            raise exception_local_to_dbus(e)
