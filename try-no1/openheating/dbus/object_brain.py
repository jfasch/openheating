from .object import DBusObject, DBusObjectCreator
from .types import DBUS_BRAIN_IFACE_STRING

from ..logic.brain import Brain

import dbus.service


class DBusBrainObject(DBusObject):
    def __init__(self, path, thinkers):
        DBusObject.__init__(self, path=path)
        self.__brain = Brain(thinkers)

    @dbus.service.method(dbus_interface=DBUS_BRAIN_IFACE_STRING, out_signature='a(ia(ss))')
    def think(self):
        return self.object_call(self.__brain.think)


class BrainObjectCreator(DBusObjectCreator):
    def __init__(self, thinkers):
        self.__thinkers = thinkers
        
    def create_object(self, path):
        return DBusBrainObject(path=path, thinkers=self.__thinkers)
