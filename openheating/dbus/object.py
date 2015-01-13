import dbus.service


class DBusObject(dbus.service.Object):
    def __init__(self, connection, path):
        dbus.service.Object.__init__(self, conn=connection.get_connection(), object_path=path)
        
