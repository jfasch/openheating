from .transport import Transport
from .thinker import Thinker
from .tendency import Tendency

from ..base import logger


class Sink(Thinker):

    def __init__(self, name, thermometer, temperature_range, diff_hysteresis, pump_switch):
        Thinker.__init__(self, name)

        self.__thermometer = thermometer
        self.__temperature_range = temperature_range
        self.__source = None

        # parameters for our transport. that will be made once we know
        # the source we are attached to.
        self.__diff_hysteresis = diff_hysteresis
        self.__pump_switch = pump_switch

        self.__transport = None

    # jjj get rid of this once we got rid of transport
    def temperature(self):
        return self.__current_temperature

    # jjj remove. no sink needs to know its source.
    def set_source(self, source):
        assert self.__source is None

        self.__source = source

        # jjj create transport. we don't need the parameters anymore,
        # so del them afterwards.
        if True:
            self.__transport = Transport(name=self.__source.name()+'->'+self.name(),
                                         source=self.__source,
                                         sink=self,
                                         diff_hysteresis=self.__diff_hysteresis, 
                                         pump_switch=self.__pump_switch)
            del self.__diff_hysteresis
            del self.__pump_switch

    def init_thinking_local(self):
        self.__transport.init_thinking_local()

        # jjj this need not be a member - it's just that Transport
        # needs it in its decisions. get rid of it once we got rid of
        # transport.
        self.__current_temperature = self.__thermometer.temperature()

        if self.__temperature_range.below(self.__current_temperature):
            # temperature below range, definitely in need for heat
            msg = '%.1f below %s -> need' % (self.__current_temperature, str(self.__temperature_range))
            self.__debug(msg)
            self.__need = True
        elif self.__temperature_range.above(self.__current_temperature):
            # temperature above range, but could still take.
            msg = '%.1f above %s -> don\'t care' % (self.__current_temperature, str(self.__temperature_range))
            self.__debug(msg)
            self.__need = None
        else:
            # temperature within range, could take heat but don't
            # need.
            msg = '%.1f within %s -> need' % (self.__current_temperature, str(self.__temperature_range))
            self.__debug(msg)
            self.__need = True

    def init_thinking_global(self):
        self.__transport.init_thinking_global()

    def think(self):
        return self.__transport.think()

    def finish_thinking_global(self):
        self.__transport.finish_thinking_global()

    def finish_thinking_local(self):
        self.__transport.finish_thinking_local()

    def test__get_need(self):
        return self.__need
    
    def __debug(self, msg):
        logger.debug('sink %s: %s' % (self.name(), msg))
