from .thinking import Thinker
from .switch import Switch

import logging

class Transport(Thinker):
    def __init__(self, name, source, sink, diff_hysteresis, pump_switch):
        self.__name = name
        self.__source = source
        self.__sink = sink
        self.__pump_switch = pump_switch
        self.__diff_hysteresis = diff_hysteresis

        sink.set_source(source)

        # my state during thinking round. None when not thinking (or
        # nothing to do after a round, at sync())
        self.__pump_open_closed = None

    def think(self):
        source_temp = self.__source.temperature()
        sink_temp = self.__sink.temperature()
        diff = source_temp - sink_temp

        requesters = self.__source.requesters()
        
        if len(requesters) and not self.__sink in requesters:
            self.__debug('pump off, somebody else needs it better: ' + ','.join(r.name() for r in requesters))
            return self.__switch_pump(Switch.OPEN)
        if self.__diff_hysteresis.above(diff):
            self.__debug('pump on')
            return self.__switch_pump(Switch.CLOSED)
        if self.__diff_hysteresis.below(diff):
            self.__debug('pump off')
            return self.__switch_pump(Switch.OPEN)

        return 0

    def sync(self):
        if self.__pump_open_closed is not None:
            self.__pump_switch.set_state(self.__pump_open_closed)
            self.__pump_open_closed = None

    def __switch_pump(self, state):
        assert state is not None
        if state != self.__pump_open_closed:
            self.__pump_open_closed = state
            return 1
        return 0

    def __debug(self, msg):
        logging.debug('transport %s: %s' % (self.__name, msg))
