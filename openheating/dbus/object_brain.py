from .object import DBusObject
from .types import DBUS_BRAIN_IFACE_STRING
from ..thinking import Brain

import dbus.service


class DBusBrainObject(DBusObject):
    def __init__(self, path, thinker):
        DBusObject.__init__(self, path=path)
        self.__thinker = thinker
        self.__brain = Brain()
        self.__thinker.register_thinking(self.__brain)

    @dbus.service.method(dbus_interface=DBUS_BRAIN_IFACE_STRING, in_signature = 's')
    def think(self, message):
        return self.object_call(self.__brain.think, message)
