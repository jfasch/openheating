from .polled import Polled

class Sink(Polled):
    def __init__(self, thermometer, hysteresis):
        self.__thermometer = thermometer
        self.__hysteresis = hysteresis
        self.__source = None
    def set_source(self, source):
        assert self.__source is None
        self.__source = source

    def poll(self):
        temperature = self.__thermometer.temperature()
        if self.__hysteresis.below(temperature):
            self.__source.request(self)
            return
        if self.__hysteresis.above(temperature):
            self.__source.release(self)
            return
