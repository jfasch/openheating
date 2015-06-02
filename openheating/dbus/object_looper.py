from .object import DBusObject, DBusObjectCreator
from .types import DBUS_LOOPER_IFACE_STRING

from ..logic.looper import Looper

import dbus.service
import dbus
from gi.repository import GObject


class DBusLooperObject(DBusObject):
    def __init__(self, path, interval, brain, triggers):
        DBusObject.__init__(self, path=path)
        self.__looper = Looper(brain=brain, triggers=triggers)
        self.__timer = GObject.timeout_add_seconds(interval, self.__expired)

    @dbus.service.method(dbus_interface=DBUS_LOOPER_IFACE_STRING, out_signature='i')
    def num_loops(self):
        return self.object_call(self.__looper.num_loops)

    def __expired(self):
        self.__looper.loop()
        return True # repeat


class LooperObjectCreator(DBusObjectCreator):
    def __init__(self, interval, brain, triggers):
        self.__interval = interval
        self.__brain = brain
        self.__triggers = triggers

    def create_object(self, path):
        return DBusLooperObject(path=path, interval=self.__interval, brain=self.__brain, triggers=self.__triggers)
