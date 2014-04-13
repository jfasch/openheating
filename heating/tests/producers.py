from ..control.producer import Producer

class TestProducer(Producer):
    def __init__(self, initial_temperature):
        self.__temperature = initial_temperature
        self.__acquired = False
    def temperature(self):
        return self.__temperature
    def acquire(self):
        self.__acquired = True
    def release(self):
        self.__acquired = False
    def is_acquired(self):
        return self.__acquired
    def set_temperature(self, temperature):
        self.__temperature = temperature
