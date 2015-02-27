from .thinking import Thinker, ThinkingSwitch
from .switch import Switch

import logging

class Transport(Thinker):
    def __init__(self, name, source, sink, diff_hysteresis, pump_switch):
        self.__name = name
        self.__source = source
        self.__sink = sink
        self.__pump_switch = ThinkingSwitch(pump_switch)
        self.__diff_hysteresis = diff_hysteresis

        sink.set_source(source)

    def start_thinking(self):
        pass

    def think(self):
        source_temp = self.__source.temperature()
        sink_temp = self.__sink.temperature()
        diff = source_temp - sink_temp

        if self.__source.num_requests() > 0 and not self.__source.is_requested_by(self.__sink):
            self.__debug('pump off, somebody else needs it better: ' + self.__source.print_requests())
            return self.__pump_switch.set(False)
        if self.__diff_hysteresis.above(diff):
            self.__debug('pump on')
            return self.__pump_switch.set(True)
        if self.__diff_hysteresis.below(diff):
            self.__debug('pump off')
            return self.__pump_switch.set(False)

        return 0

    def stop_thinking(self):
        self.__pump_switch.sync()

    def __debug(self, msg):
        logging.debug('transport %s: %s' % (self.__name, msg))
