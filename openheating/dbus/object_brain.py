from .object import DBusObject
from .types import DBUS_BRAIN_IFACE_STRING

from ..logic.brain import Brain

import dbus.service


class DBusBrainObject(DBusObject):
    def __init__(self, path, thinkers):
        DBusObject.__init__(self, path=path)
        self.__brain = Brain(thinkers)

    @dbus.service.method(dbus_interface=DBUS_BRAIN_IFACE_STRING, in_signature = 's')
    def think(self, message):
        return self.object_call(self.__brain.think, message)
