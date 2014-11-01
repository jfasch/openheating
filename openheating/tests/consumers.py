from ..consumer import Consumer

class TestConsumer(Consumer):
    def __init__(self, wanted_temperature, initial_temperature):
        self.__wanted_temperature = wanted_temperature
        self.__temperature = initial_temperature
    def temperature(self):
        return self.__temperature
    def wanted_temperature(self):
        return self.__wanted_temperature
    def set_temperature(self, temperature):
        self.__temperature = temperature
