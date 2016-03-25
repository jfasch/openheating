from .transport import Transport
from .thinker import Thinker
from .tendency import Tendency

from ..base import logger


class Sink(Thinker):

    def __init__(self, name, thermometer, temperature_range, diff_hysteresis, pump_switch):
        Thinker.__init__(self, name)

        self.__thermometer = thermometer
        self.__pump_switch = pump_switch
        self.__temperature_range = temperature_range
        self.__diff_hysteresis = diff_hysteresis
        self.__source = None

    def set_source(self, source):
        assert self.__source is None
        self.__source = source

    def init_thinking_local(self):
        self.__think__sink_temperature = self.__thermometer.temperature()
        self.__think__need = None

    def init_thinking_global(self):
        self.__think__source_temperature = self.__source.temperature()

    def think(self):
        thoughts = []

        # see if we need temperature. my source is then able to react
        # accordingly, and possibly produce heat.
        if self.__temperature_range.below(self.__think__sink_temperature):
            # temperature below range, definitely in need for heat
            if self.__think__need is not True:
                msg = '%.1f below %s -> need' % (self.__think__sink_temperature, str(self.__temperature_range))
                self.__debug(msg)
                self.__think__need = True
                thoughts.append((self.name(), msg))
        elif self.__temperature_range.above(self.__think__sink_temperature):
            # temperature above range, but could still take.
            if self.__think__need is not False:
                msg = '%.1f above %s -> don\'t need' % (self.__think__sink_temperature, str(self.__temperature_range))
                self.__debug(msg)
                self.__think__need = False
                thoughts.append((self.name(), msg))

        return thoughts

    def finish_thinking_local(self):
        # compare source and sink temperatures, and switch on/off pump
        # accordingly.
        difference = self.__think__source_temperature - self.__think__sink_temperature

        if self.__diff_hysteresis.above(difference):
            msg = 'pump on (source %.1f - sink %.1f) is above %s' % \
                  (round(self.__think__source_temperature, 1), 
                   round(self.__think__sink_temperature, 1), 
                   str(self.__diff_hysteresis))
            self.__debug(msg)
            self.__pump_switch.set_state(True)
        elif self.__diff_hysteresis.below(difference):
            msg = 'pump off (source %.1f - sink %.1f) is below %s' % \
                  (round(self.__think__source_temperature, 1), 
                   round(self.__think__sink_temperature, 1), 
                   str(self.__diff_hysteresis))
            self.__debug(msg)
            self.__pump_switch.set_state(False)

        del self.__think__sink_temperature
        del self.__think__source_temperature
        del self.__think__need

    def __debug(self, msg):
        logger.debug('sink %s: %s' % (self.name(), msg))
