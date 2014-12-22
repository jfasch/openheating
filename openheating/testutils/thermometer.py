from ..thermometer import Thermometer

class TestThermometer(Thermometer):
    def __init__(self, initial_temperature):
        self.__temperature = initial_temperature
        self.__num_calls = 0

    def temperature(self):
        self.__num_calls += 1
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def num_calls(self):
        return self.__num_calls
