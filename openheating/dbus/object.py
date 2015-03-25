from .connection import DBusServerConnection

import dbus.service


class DBusObject(dbus.service.Object):
    def __init__(self, connection, path):
        assert isinstance(connection, DBusServerConnection)
        dbus.service.Object.__init__(self, conn=connection.get_connection(), object_path=path)
