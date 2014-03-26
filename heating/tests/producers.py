from ..control.producer import Producer

class TestProducer(Producer):
    def __init__(self, initial_temperature):
        self.__temperature = initial_temperature
        self.__peeked = False
    def temperature(self):
        return self.__temperature
    def peek(self):
        self.__peeked = True
    def peeked(self):
        return self.__peeked
