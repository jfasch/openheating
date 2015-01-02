'''"rebinding" wrappers of both DBus connections and DBus objects.

DBus connections and objects tend to break on connection loss on
either side. If a client connection to the bus breaks, all is lost. If
an object's reference to a service/object breaks due to it's loss of
connection to the bus, then the local object proxy is dead.

openheating's use of objects is through instances of DBusObjectClient
(one is supposed to derive from it), and the overall
DBusConnectionProxy which is instantiated once and passed in. Recovery
is done inside, on both connections and objects.

'''

from .types import exception_dbus_to_local
from ..error import HeatingError, DBusNoConnectionError, DBusNoServiceError

from dbus.exceptions import DBusException
import dbus.bus

class DBusConnectionProxy:
    '''Recovery of DBus connection

    User code instantiates one and passes it to DBusObjectClient
    instances which do the rest.

    '''

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
    '''Recovery of DBus object proxy

    User code is supposed to derive and implement its methods using
    base's dbus_call(), with the name of the method and positional
    parameters. (Keyword parameters are not supported, as this is not
    the nature of the DBus protocol).

    '''
    
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
        
