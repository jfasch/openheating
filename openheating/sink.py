from .thinking import Thinker
from .tendency import Tendency

import logging


class Sink(Thinker):
    def __init__(self, name, thermometer, temperature_range):
        Thinker.__init__(self, name)

        self.__thermometer = thermometer
        self.__temperature_range = temperature_range
        self.__source = None
        self.__requesting = False

        # request desired upper bound plus 3. this is pretty
        # arbitrary.

        # for example, if we are a boiler (hot water reservoir), then
        # our upper bound will be at about 80. requesting 83 at a wood
        # oven will fail, whereas 83 at a oil oven will succeed. and
        # that's the plan after all.

        # anyway, let's see where all this leads us.
        self.__requested_temperature = temperature_range.high() + 3

    def set_source(self, source):
        assert self.__source is None
        self.__source = source

    def temperature(self):
        return self.__current_temperature

    def register_thinking(self, brain):
        brain.register_thinker(self)

    def init_thinking_local(self):
        self.__current_temperature = self.__thermometer.temperature()
        self.__decision_made = False

    def finished_thinking(self):
        del self.__current_temperature
        del self.__decision_made

    def think(self):
        if self.__decision_made:
            return 0
        self.__decision_made = True

        # temperature below range, have to request
        if self.__temperature_range.below(self.__current_temperature):
            self.__debug('%f below (%f,%f), requesting')
            self.__requesting = True
            self.__source.request(self, self.__requested_temperature)
            return 1

        # temperature above range, no request
        if self.__temperature_range.above(self.__current_temperature):
            self.__debug('%f above (%f,%f), not requesting')
            self.__requesting = False
            return 1

        # temperature within range. keep requesting if we were already
        # (we are just heating up). else, we are cooling and don't
        # request.
        if self.__requesting:
            self.__debug('%f within (%f,%f), keep requesting')
            self.__source.request(self, self.__requested_temperature)
            return 1

        return 0

    def __debug(self, msg):
        logging.debug('sink %s: %s' % (self.name(), msg))
