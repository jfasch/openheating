from .connection import DBusServerConnection

import dbus.service

import sys


class DBusObject(dbus.service.Object):
    def __init__(self, path):
        if not DBusServerConnection.instance:
            # print this out loudly; the AssertionError appears to get
            # lost somewhere deep inside dbus.
            print('FATAL: DBusObject: DBusServerConnection.instance is not set', file=sys.stderr)
            assert False

        dbus.service.Object.__init__(self, conn=DBusServerConnection.instance.get_connection(), object_path=path)
