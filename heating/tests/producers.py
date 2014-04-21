from ..control.producer_backend import ProducerBackend

class TestProducerBackend(ProducerBackend):
    def __init__(self, initial_temperature):
        self.__temperature = initial_temperature
        self.__producing = False
        self.__needs_cooling = False
    def temperature(self):
        return self.__temperature
    def start_producing(self):
        self.__producing = True
    def stop_producing(self):
        self.__producing = False
    def needs_cooling(self):
        return self.__needs_cooling

    def is_producing(self):
        return self.__producing
    def set_temperature(self, temperature):
        self.__temperature = temperature
