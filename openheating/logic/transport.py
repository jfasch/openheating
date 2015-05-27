from .thinker import LeafThinker
from .switch import Switch

from ..base import logger


class Transport(LeafThinker):
    def __init__(self, name, source, sink, diff_hysteresis, pump_switch):
        LeafThinker.__init__(self, name)

        self.__source = source
        self.__sink = sink
        self.__pump_switch = pump_switch
        self.__diff_hysteresis = diff_hysteresis

        sink.set_source(source)

    def init_thinking_local(self):
        self.__difference = self.__source.temperature() - self.__sink.temperature()
        self.__switch_state = None
        self.__decision_made = False

    def finish_thinking_local(self):
        if self.__switch_state is not None:
            self.__pump_switch.set_state(self.__switch_state)
        del self.__switch_state

    def think(self):
        if self.__source.num_requests() > 0 and not self.__source.is_requested_by(self.__sink):
            msg = 'pump off, somebody else needs it better: ' + self.__source.print_requests()
            self.__debug(msg)
            return self.__think_set_switch_state(False, msg)
        if self.__diff_hysteresis.above(self.__difference):
            msg = 'pump on'
            self.__debug(msg)
            return self.__think_set_switch_state(True, msg)
        if self.__diff_hysteresis.below(self.__difference):
            msg = 'pump off'
            self.__debug(msg)
            return self.__think_set_switch_state(False, msg)
        return []

    def __debug(self, msg):
        logger.debug('transport %s: %s' % (self.name(), msg))

    def __think_set_switch_state(self, state, msg):
        if self.__switch_state == state:
            return []
        else:
            self.__switch_state = state
            return [(self.name(), msg)]
