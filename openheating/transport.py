from .polling import Polled

import logging

class Transport(Polled):
    def __init__(self, name, source, sink, diff_hysteresis, pump_switch):
        self.__name = name
        self.__source = source
        self.__sink = sink
        self.__pump_switch = pump_switch
        self.__diff_hysteresis = diff_hysteresis

        sink.set_source(source)

    def poll(self):
        source_temp = self.__source.temperature()
        sink_temp = self.__sink.temperature()
        diff = source_temp - sink_temp

        if self.__diff_hysteresis.above(diff):
            self.__debug('pump on')
            self.__pump_switch.on()
            return
        if self.__diff_hysteresis.below(diff):
            self.__debug('pump off')
            self.__pump_switch.off()
            return

    def __debug(self, msg):
        logging.debug('transport %s: %s' % (self.__name, msg))
