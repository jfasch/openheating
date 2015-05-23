from ..base import logger

import dbus
import dbus.bus

from abc import ABCMeta, abstractmethod
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
    reason.
    '''

    # when living in a service process, there ought to be only one
    # connection.
    instance = None
    
    def __init__(self, connection):
        self.__connection = connection
    
    def get_proxy(self, name, path):
        return self.__connection.get_object(name, path)

    def connection_lost(self):
        logger.error('server connection lost')
        os._exit(1)

    def get_connection(self):
        ''' Specific to this class, used to create DBus Objects with
        '''
        return self.__connection

