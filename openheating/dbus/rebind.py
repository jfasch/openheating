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

from . import types
from ..error import HeatingError

from dbus.exceptions import DBusException
import dbus.bus

from abc import ABCMeta, abstractmethod
import logging
import os


class DBusConnection(metaclass=ABCMeta):
    @abstractmethod
    def get_proxy(self, name, path):
        pass
    @abstractmethod
    def connection_lost(self):
        pass

class DBusClientConnection(DBusConnection):
    '''Implements recovery of DBus connection, by-address

    A connection is (re)established on get_connection(). this is the
    "client mode"; it works best when used with DBusObjectClient which
    does all the rest.  '''

    def __init__(self, address):
        self.__address = address
        self.__connection = None

    def get_proxy(self, name, path):
        if self.__connection is None:
            self.__connection = dbus.bus.BusConnection(self.__address)
        return self.__connection.get_object(name, path)

    def connection_lost(self):
        self.__connection = None

class DBusServerConnection(DBusConnection):
    '''Encapsulates a pre-existing DBus connection

    This is the "server mode", where a connection pre-exists, and the
    server process terminates once the connection goes down for some
    reason. Best used together with DBusServiceCombo.
    '''
    
    def __init__(self, connection):
        self.__connection = connection
    
    def get_proxy(self, name, path):
        return self.__connection.get_object(name, path)

    def connection_lost(self):
        logging.error('server connection lost')
        os._exit(1)

    def get_connection(self):
        ''' Specific to this class, used to create DBus Objects with
        '''
        return self.__connection

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
        self.__proxy = None

    def dbus_call(self, funcname, *args):
        exc = None
        try:
            if self.__proxy is None:
                self.__proxy = self.__connection.get_proxy(self.__name, self.__path)
            func = self.__proxy.get_dbus_method(funcname)
            return func(*args)

        except DBusException as e:
            exc_name = e.get_dbus_name()
            exc_msg = e.get_dbus_message()

            if exc_name == types.DBUS_HEATING_ERROR_NAME:
                # HeatingError pass-through from the remote side.
                raise types.exception_dbus_to_local(e)

            if exc_name in ('org.freedesktop.DBus.Error.NoServer',
                            'org.freedesktop.DBus.Error.Disconnected',
                            # TCP: EHOSTUNREACH as it seems
                            'org.freedesktop.DBus.Error.Failed',
                            # TCP: ENETUNREACH as it seems
                            'org.freedesktop.DBus.Error.NoNetwork',
                            # UNIX: server socket not there
                            'org.freedesktop.DBus.Error.FileNotFound',
                            ):
                msg = 'dbus error: connection problem: '+str(e)
                logging.warning(msg)
                self.__proxy = None
                self.__connection.connection_lost()
                raise HeatingError(msg)

            if exc_name in ('org.freedesktop.DBus.Error.NoReply',
                            'org.freedesktop.DBus.Error.NameHasNoOwner',
                            'org.freedesktop.DBus.Error.ServiceUnknown',
                            ):
                msg = 'dbus error: object problem: '+str(e)
                logging.warning(msg)
                self.__proxy = None
                raise HeatingError(msg)

            self.__connection.connection_lost()
            assert False, "can't let this one pass: "+str(e)
