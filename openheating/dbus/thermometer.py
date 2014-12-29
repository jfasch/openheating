from ..thermometer import Thermometer
from ..error import HeatingException

from dbus.exceptions import DBusException

class DBusThermometer(Thermometer):
    def __init__(self, connection, name, path):
        self.__object = connection.get_object(name, path)
    def temperature(self):
        try:
            return float(self.__object.temperature())
        except DBusException as e:
            raise HeatingException(msg='remote error', nested_errors=[e])
                      
