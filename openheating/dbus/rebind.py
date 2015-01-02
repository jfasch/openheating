from .types import exception_dbus_to_local
from ..error import HeatingError, DBusNoConnectionError, DBusNoServiceError

from dbus.exceptions import DBusException
import dbus.bus

class DBusConnectionProxy:
    def __init__(self, address):
        self.__address = address
        self.__connection = None

    def get_connection(self):
        if self.__connection is None:
            self.__connection = dbus.bus.BusConnection(self.__address)
        return self.__connection

    def clear_connection(self):
        self.__connection = None

class DBusObjectClient:
    def __init__(self, connection_proxy, name, path):
        self.__connection_proxy = connection_proxy
        self.__name = name
        self.__path = path
        self.__object = None

    def dbus_call(self, funcname, *args):
        try:
            if self.__object is None:
                self.__object = self.__connection_proxy.get_connection().get_object(self.__name, self.__path)
            func = self.__object.get_dbus_method(funcname)
            return func(*args)
        except DBusException as e:
            if e.get_dbus_name() in ('org.freedesktop.DBus.Error.Disconnected', 'org.freedesktop.DBus.Error.NoServer'):
                self.__connection_proxy.clear_connection()
                self.__object = None
                raise DBusNoConnectionError(msg=str(e))
            if e.get_dbus_name() in ('org.freedesktop.DBus.Error.ServiceUnknown'):
                self.__object = None
                raise DBusNoServiceError(msg=str(e))
            raise exception_dbus_to_local(e)
        
