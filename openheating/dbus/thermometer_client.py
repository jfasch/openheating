from .types import exception_dbus_to_local

from ..thermometer import Thermometer
from ..error import HeatingError, DBusNoConnectionError, DBusNoServiceError

from dbus.exceptions import DBusException


class DBusThermometer(Thermometer):
    def __init__(self, connection_proxy, name, path):
        self.__connection_proxy = connection_proxy
        self.__name = name
        self.__path = path
        self.__object = None
    def temperature(self):
        try:
            if self.__object is None:
                self.__object = self.__connection_proxy.get_connection().get_object(self.__name, self.__path)
            return float(self.__object.temperature())
        except DBusException as e:
            if e.get_dbus_name() in ('org.freedesktop.DBus.Error.Disconnected', 'org.freedesktop.DBus.Error.NoServer'):
                self.__connection_proxy.clear_connection()
                self.__object = None
                raise DBusNoConnectionError(msg=str(e))
            if e.get_dbus_name() in ('org.freedesktop.DBus.Error.ServiceUnknown'):
                self.__object = None
                raise DBusNoServiceError(msg=str(e))
            raise exception_dbus_to_local(e)
