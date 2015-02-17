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

    def think(self):
        source_temp = self.__source.temperature()
        sink_temp = self.__sink.temperature()
        diff = source_temp - sink_temp

        requesters = self.__source.requesters()
        
        if len(requesters) and not self.__sink in requesters:
            self.__debug('pump off, somebody else needs it better: ' + ','.join(r.name() for r in requesters))
            return self.__pump_switch.set(False)
        if self.__diff_hysteresis.above(diff):
            self.__debug('pump on')
            return self.__pump_switch.set(True)
        if self.__diff_hysteresis.below(diff):
            self.__debug('pump off')
            return self.__pump_switch.set(False)

        return 0

    def sync(self):
        self.__pump_switch.sync()
        self.__pump_switch.reset()

    def __debug(self, msg):
        logging.debug('transport %s: %s' % (self.__name, msg))
