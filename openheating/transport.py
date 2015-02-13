from .thinking import Thinker
from .switch import Switch

import logging

class Transport(Thinker):
    def __init__(self, name, source, sink, diff_hysteresis, pump_switch):
        self.__name = name # for debugging
        self.__source = source
        self.__sink = sink
        self.__pump_switch = pump_switch
        self.__diff_hysteresis = diff_hysteresis

        sink.set_transport(self)

        # my state during thinking round. None when not thinking (or
        # nothing to do after a round, at sync())
        self.__pump_open_closed = None

    def name(self):
        return self.__name

    def request(self):
        self.__source.request(self)
    def release(self):
        self.__source.release(self)

    def think(self):
        '''Thinker implementation'''

        source_temp = self.__source.temperature()
        sink_temp = self.__sink.temperature()
        diff = source_temp - sink_temp

        requesters = self.__source.requesters()

        if len(requesters) and not self in requesters:
            self.__debug('pump off, somebody else needs it better: ' + ','.join(t.name() for t in requesters))
            return self.__switch_pump(False)
        if self.__diff_hysteresis.above(diff):
            self.__debug('pump on')
            return self.__switch_pump(True)
        if self.__diff_hysteresis.below(diff):
            self.__debug('pump off')
            return self.__switch_pump(False)

        return 0

    def sync(self):
        '''Thinker implementation'''
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
