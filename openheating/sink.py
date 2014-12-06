from .polling import Polled

import logging

class Sink(Polled):
    def __init__(self, name, thermometer, hysteresis):
        self.__name = name
        self.__thermometer = thermometer
        self.__hysteresis = hysteresis
        self.__source = None

    def set_source(self, source):
        assert self.__source is None
        self.__source = source

    def temperature(self):
        return self.__thermometer.temperature()

    def poll(self):
        temperature = self.__thermometer.temperature()
        if self.__hysteresis.below(temperature):
            self.__debug('request')
            self.__source.request(self)
            return
        if self.__hysteresis.above(temperature):
            self.__debug('release')
            self.__source.release(self)
            return

    def __debug(self, msg):
        logging.debug('sink %s: %s' % (self.__name, msg))
