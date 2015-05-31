from .object import DBusObject, DBusObjectCreator
from .types import DBUS_SWITCH_CENTER_IFACE_STRING

from ..logic.switch_center import SwitchCenter

import dbus
import dbus.service


class DBusSwitchCenterObject(DBusObject):
    '''Adapt a SwitchCenter into a DBus object at object_path'''

    def __init__(self, path, center):
        self.__center = center
        DBusObject.__init__(self, path=path)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_CENTER_IFACE_STRING, out_signature='as')
    def all_names(self):
        return self.object_call(self.__center.all_names)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_CENTER_IFACE_STRING, in_signature = 'sb')
    def set_state(self, name, value):
        # have to convert value from "dbus.Boolean" which slips
        # through upon us
        return self.object_call(self.__center.set_state, name, value and True or False)

    @dbus.service.method(dbus_interface=DBUS_SWITCH_CENTER_IFACE_STRING, in_signature='s', out_signature = 'b')
    def get_state(self, name):
        return self.object_call(self.__center.get_state, name)


class SwitchCenterObjectCreator(DBusObjectCreator):
    def __init__(self, switches):
        self.__switches = switches
        
    def create_object(self, path):
        return DBusSwitchCenterObject(
            path=path,
            center=SwitchCenter(self.__switches))
