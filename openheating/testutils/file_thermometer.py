from ..thermometer import Thermometer

class FileThermometer(Thermometer):
    def __init__(self, path):
        self.__path = path
    def temperature(self):
        return float(open(self.__path).read())
        
