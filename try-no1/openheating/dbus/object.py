from .connection import DBusServerConnection
from .types import exception_local_to_dbus

from ..base.error import HeatingError
from ..base import logger

import dbus.service

from abc import ABCMeta, abstractmethod
import sys


class DBusObject(dbus.service.Object):
    def __init__(self, path):
        if not DBusServerConnection.instance:
            # print this out loudly; the AssertionError appears to get
            # lost somewhere deep inside dbus.
            print('FATAL: DBusObject: DBusServerConnection.instance is not set', file=sys.stderr)
            assert False

        dbus.service.Object.__init__(self, conn=DBusServerConnection.instance.get_connection(), object_path=path)
        self.__path = path

    def object_call(self, callable, *args):
        try:
            return callable(*args)
        except HeatingError as e:
            logger.exception('%s: heating error: %s' % (self.__path, str(e)))
            raise exception_local_to_dbus(e)
        except Exception as e:
            logger.exception('%s: unknown error: %s' % (self.__path, str(e)))
            raise
        
class DBusObjectCreator(metaclass=ABCMeta):
    @abstractmethod
    def create_object(self, path):
        pass

