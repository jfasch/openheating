from .types import exception_dbus_to_local

from ..thermometer import Thermometer
from ..error import HeatingError

from dbus.exceptions import DBusException


class DBusThermometer(Thermometer):
    def __init__(self, connection, name, path):
        self.__object = connection.get_object(name, path)
    def temperature(self):
        try:
            return float(self.__object.temperature())
        except DBusException as e:
            print('jjj>>>>>>>>>>>>>>>>>>>\n', str(e), 'jjj<<<<<<<<<<<<<<<<<\n')
            raise exception_dbus_to_local(e)
