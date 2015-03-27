from .object import DBusObject
from .types import DBUS_SWITCH_IFACE_STRING

import dbus.service


class DBusSwitchObject(DBusObject):
    '''Adapt a Switch into a DBus object at object_path'''

    def __init__(self, path, switch):
        DBusObject.__init__(self, path=path)
        self.__switch = switch

    @dbus.service.method(dbus_interface=DBUS_SWITCH_IFACE_STRING, in_signature = 'b')
    def set_state(self, value):
        # have to convert value from "dbus.Boolean" which slips
        # through upon us
        return self.object_call(self.__switch.set_state, value and True or False)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_IFACE_STRING, out_signature = 'b')
    def get_state(self):
        return self.object_call(self.__switch.get_state)
