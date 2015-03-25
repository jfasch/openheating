from .object import DBusObject
from .types import exception_local_to_dbus, DBUS_BRAIN_IFACE_STRING

from ..error import HeatingError
from ..thinking import Brain

from ..jf_control import JFControl

import dbus.service


class JFControlObject(DBusObject):
    def __init__(self, path, jf_control):
        DBusObject.__init__(self, path=path)
        self.__jf_control = jf_control
        self.__brain = Brain()
        self.__jf_control.register_thinking(self.__brain)

    @dbus.service.method(dbus_interface=DBUS_BRAIN_IFACE_STRING, in_signature = 'b')
    def think(self, message):
        try:
            self.__brain.think(message)
        except HeatingError as e:
            raise exception_local_to_dbus(e)
