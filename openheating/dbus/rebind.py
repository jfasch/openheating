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

from abc import ABCMeta, abstractmethod


class DBusConnection(metaclass=ABCMeta):
    @abstractmethod
    def get_connection(self):
        pass
    @abstractmethod
    def clear_connection(self):
        pass

class DBusClientConnection(DBusConnection):
    '''Implements recovery of DBus connection, by-address

    A connection is (re)established on get_connection(). this is the
    "client mode"; it works best when used with DBusObjectClient which
    does all the rest.  '''

    def __init__(self, address):
        self.__address = address
        self.__connection = None

    def get_connection(self):
        if self.__connection is None:
            self.__connection = dbus.bus.BusConnection(self.__address)
        return self.__connection

    def clear_connection(self):
        self.__connection = None

class DBusServerConnection(DBusConnection):
    '''Encapsulates a pre-existing DBus connection

    This is the "server mode", where a connection pre-exists, and the
    server process terminates once the connection goes down for some
    reason. Best used together with DBusServiceCombo.
    '''
    
    def __init__(self, connection):
        self.__connection = connection
    
    def get_connection(self):
        return self.__connection

    def clear_connection(self):
        raise HeatingError('server connection: client error: connection closed')

class DBusObjectClient:
    '''Recovery of DBus object proxy

    User code is supposed to derive and implement its methods using
    base's dbus_call(), with the name of the method and positional
    parameters. (Keyword parameters are not supported, as this is not
    the nature of the DBus protocol).

    '''
    
    def __init__(self, connection, name, path):
        self.__connection = connection
        self.__name = name
        self.__path = path
        self.__object = None

    def dbus_call(self, funcname, *args):
        try:
            if self.__object is None:
                self.__object = self.__connection.get_connection().get_object(self.__name, self.__path)
            func = self.__object.get_dbus_method(funcname)
            return func(*args)
        except DBusException as e:
            if e.get_dbus_name() in ('org.freedesktop.DBus.Error.Disconnected',
                                     'org.freedesktop.DBus.Error.NoServer',
                                     'org.freedesktop.DBus.Error.NoReply',
                                     # EHOSTUNREACH as it seems
                                     'org.freedesktop.DBus.Error.Failed',
                                     # ENETUNREACH as it seems
                                     'org.freedesktop.DBus.Error.NoNetwork',
                                     ):
                self.__connection.clear_connection()
                self.__object = None
                raise DBusNoConnectionError(msg=str(e))
            if e.get_dbus_name() in ('org.freedesktop.DBus.Error.ServiceUnknown'):
                self.__object = None
                raise DBusNoServiceError(msg=str(e))
            raise exception_dbus_to_local(e)
        
