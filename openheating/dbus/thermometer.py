from ..thermometer import Thermometer

class DBusThermometer(Thermometer):
    def __init__(self, connection, name, path):
        self.__object = connection.get_object(name, path)
    def temperature(self):
        return float(self.__object.temperature())
                      
