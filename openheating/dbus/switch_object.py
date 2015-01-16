from .object import DBusObject
from .types import exception_local_to_dbus, DBUS_SWITCH_IFACE_STRING

from ..switch import Switch
from ..error import HeatingError

import dbus
import dbus.service


class DBusSwitchObject(dbus.service.Object):
    '''Adapt a Switch into a DBus object at object_path'''

    def __init__(self, connection, path, switch):
        DBusObject.__init__(self, connection=connection, path=path)
        self.__switch = switch

    @dbus.service.method(dbus_interface=DBUS_SWITCH_IFACE_STRING, in_signature = 'b')
    def set_state(self, value):
        try:
            self.__switch.set_state(value and Switch.CLOSED or Switch.OPEN)
        except HeatingError as e:
            raise exception_local_to_dbus(e)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_IFACE_STRING, out_signature = 'b')
    def get_state(self):
        try:
            value = self.__switch.get_state()
            if value == Switch.OPEN:
                return False
            elif value == Switch.CLOSED:
                return True
            else:
                assert False, value
        except HeatingError as e:
            raise exception_local_to_dbus(e)
