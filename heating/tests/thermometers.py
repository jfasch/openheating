from heating.thermometer import Thermometer

class TestThermometer(Thermometer):
    def __init__(self, initial_temperature):
        self.__temperature = initial_temperature
    def temperature(self):
        return self.__temperature
    def set_temperature(self, temperature):
        self.__temperature = temperature
