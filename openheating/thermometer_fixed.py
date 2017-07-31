from .thermometer import Thermometer


class FixedThermometer(Thermometer):
    def __init__(self, temperature):
        self.__temperature = temperature

    def get_temperature(self):
        return self.__temperature
