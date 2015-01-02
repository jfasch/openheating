import dbus.bus

class DBusConnectionProxy:
    def __init__(self, address):
        self.__address = address
        self.__connection = None

    def get_connection(self):
        if self.__connection is None:
            self.__connection = dbus.bus.BusConnection(self.__address)
        return self.__connection

    def clear_connection(self):
        self.__connection = None
