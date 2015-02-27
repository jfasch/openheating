from .thinking import Thinker
from .tendency import Tendency

import logging


class Sink(Thinker):
    def __init__(self, name, thermometer, temperature_range):
        self.__name = name
        self.__thermometer = thermometer
        self.__temperature_range = temperature_range
        self.__source = None
        self.__tendency = Tendency()

        # request desired upper bound plus 3. this is pretty
        # arbitrary.

        # for example, if we are a boiler (hot water reservoir), then
        # our upper bound will be at about 80. requesting 83 at a wood
        # oven will fail, whereas 83 at a oil oven will succeed. and
        # that's the plan after all.

        # anyway, let's see where all this leads us.
        self.__requested_temperature = temperature_range.high() + 3

    def name(self):
        return self.__name

    def set_source(self, source):
        assert self.__source is None
        self.__source = source

    def temperature(self):
        return self.__current_temperature

    def start_thinking(self):
        self.__current_temperature = self.__thermometer.temperature()
        self.__tendency.add(self.__current_temperature)
        self.__decision_made = False

    def stop_thinking(self):
        del self.__current_temperature
        del self.__decision_made

    def think(self):
        if self.__decision_made:
            return 0
        self.__decision_made = True

        if self.__temperature_range.below(self.__current_temperature):
            self.__debug('request(below)')
            self.__do_request()
            return 1
        if self.__temperature_range.between(self.__current_temperature) and self.__tendency.rising():
            self.__debug('request(between and rising)')
            self.__do_request()
            return 1
        return 0

    def __do_request(self):
        self.__source.request(self, self.__requested_temperature)
        
    def __debug(self, msg):
        logging.debug('sink %s: %s' % (self.__name, msg))
