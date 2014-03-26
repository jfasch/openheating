from ..control.producer import Producer

class TestProducer(Producer):
    def __init__(self, initial_temperature):
        self.__temperature = initial_temperature
    def temperature(self):
        return self.__temperature

