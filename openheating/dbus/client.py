from . import types
from ..error import HeatingError

from dbus.exceptions import DBusException
import dbus.bus

import logging


class DBusObjectClient:
    '''Recovery of DBus object proxy

    User code is supposed to derive and implement its methods using
    base's dbus_call(), with the name of the method and positional
    parameters. (Keyword parameters are not supported, as this is not
    the nature of the DBus protocol).

    As for the connection parameter: there are two different use cases
    for DBusObjectClient, depending on where they live.

    * In a DBus client program. There, one makes an explicit
      connection, instantiates proxies (DBusObjectClient's), and uses
      them. Here the connection is passed to the constructor, and the
      object uses it.

    * In a DBus service (or "dbus object", respectively). The DBus
      service creates a connection at startup, and then passes that
      connection to the dbus objects that it hosts. The dbus objects
      then may create DBusObjectClient instances as they start up. In
      order for configuration to stay transparent (at configuration
      time we don't have a connection), we use a class (yes!)
      variable "service_dbus_connection" for that.

    '''

    service_dbus_connection = None

    def __init__(self, name, path, connection=None):
        if connection:
            self.__connection = connection
        else:
            self.__connection = self.service_dbus_connection
            
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
