from .thinker import Thinker
from .switch import Switch
from . import logger


class Transport(Thinker):
    def __init__(self, name, source, sink, diff_hysteresis, pump_switch):
        Thinker.__init__(self, name)

        self.__source = source
        self.__sink = sink
        self.__pump_switch = pump_switch
        self.__diff_hysteresis = diff_hysteresis

        sink.set_source(source)

    def register_thinking(self, brain):
        super().register_thinking(brain)
        brain.register_thinker(self)

    def finish_thinking_global(self):
        super().finish_thinking_global()

        diff = self.__source.temperature() - self.__sink.temperature()

        if self.__source.num_requests() > 0 and not self.__source.is_requested_by(self.__sink):
            self.__debug('pump off, somebody else needs it better: ' + self.__source.print_requests())
            return self.__pump_switch.do_open()
        if self.__diff_hysteresis.above(diff):
            self.__debug('pump on')
            return self.__pump_switch.do_close()
        if self.__diff_hysteresis.below(diff):
            self.__debug('pump off')
            return self.__pump_switch.do_open()

    def __debug(self, msg):
        logger.debug('transport %s: %s' % (self.name(), msg))
