from .thinking import Thinker

import logging

class Sink(Thinker):
    def __init__(self, name, thermometer, hysteresis):
        self.__name = name
        self.__thermometer = thermometer
        self.__hysteresis = hysteresis
        self.__source = None

        self.__thinking = False

    def name(self):
        return self.__name

    def set_source(self, source):
        assert self.__source is None
        self.__source = source

    def temperature(self):
        return self.__thermometer.temperature()

    def think(self):
        if self.__thinking:
            # story already told
            return 0

        self.__thinking = True

        nthoughts = 0
        temperature = self.__thermometer.temperature()
        if self.__hysteresis.below(temperature):
            self.__debug('request')
            self.__source.request(self)
            nthoughts += 1
        elif self.__hysteresis.above(temperature):
            self.__debug('release')
            self.__source.release(self)
            nthoughts += 1
        else:
            self.__debug('nop')
        return nthoughts

    def sync(self):
        self.__thinking = False

    def __debug(self, msg):
        logging.debug('sink %s: %s' % (self.__name, msg))
