from .source import Source
from .thinking import Thinker
from .tendency import Tendency

import logging


class OilWoodCombination(Source, Thinker):

    OIL, OIL_FADE_OUT, WOOD, WOOD_FADE_OUT = 0, 1, 2, 3

    def __init__(self, name, oil, wood, valve_switch, wood_warm, wood_hot):
        assert wood_hot.low() - wood_warm.high() >= 6

        self.__name = name
        self.__oil = oil
        self.__wood = wood
        self.__wood_warm = wood_warm
        self.__wood_hot = wood_hot
        self.__valve_switch = valve_switch
        self.__wood_tendency = Tendency()
        self.__state = self.OIL

    def start_thinking(self):
        self.__oil.start_thinking()
        self.__wood.start_thinking()

        self.__oil_temperature = self.__oil.temperature()
        self.__wood_temperature = self.__wood.temperature()

        self.__wood_tendency.add(self.__wood_temperature)

        # between either of the hysteresis ranges. undecided; state
        # left as-is, but do some debug output
        if self.__wood_warm.between(self.__wood_temperature):
            self.__change_state(self.__state, 'within wood-warm hysteresis range')
            return
        elif self.__wood_hot.between(self.__wood_temperature):
            self.__change_state(self.__state, 'within wood-hot hysteresis range')
            return

        # wood above hot -> clearly wood
        elif self.__wood_hot.above(self.__wood_temperature):
            self.__change_state(self.WOOD, 'wood is hot')
            return
        # wood below warm -> clearly oil
        elif self.__wood_warm.below(self.__wood_temperature):
            self.__change_state(self.OIL, 'wood is cold')
            return

        # wood between warm and hot; let tendency rule
        elif self.__wood_tendency.rising():
            self.__change_state(self.OIL_FADE_OUT, 'warm/hot, rising')
            return
        elif self.__wood_tendency.falling():
            self.__change_state(self.WOOD_FADE_OUT, 'warm/hot, falling')
            return
        else:
            # no tendency, leave state as-is
            self.__change_state(self.__state, 'fading, but no tendency')

    def stop_thinking(self):
        self.__oil.stop_thinking()
        self.__wood.stop_thinking()
        
        del self.__wood_temperature
        del self.__oil_temperature

        if self.__state == self.OIL:
            self.__valve_switch.do_open()
        elif self.__state == self.OIL_FADE_OUT:
            self.__valve_switch.do_open()
        elif self.__state == self.WOOD:
            self.__valve_switch.do_close()
        elif self.__state == self.WOOD_FADE_OUT:
            self.__valve_switch.do_close()
        else:
            assert False
            
    def think(self):
        # me not thinking, me only delegating
        return self.__oil.think() + self.__wood.think()

    def request(self, sink, temperature):
        if self.__state == self.OIL:
            return self.__oil.request(sink, temperature)
        elif self.__state == self.OIL_FADE_OUT:
            return self.__wood.request(sink, temperature)
        elif self.__state == self.WOOD:
            return self.__wood.request(sink, temperature)
        elif self.__state == self.WOOD_FADE_OUT:
            return self.__wood.request(sink, temperature)
        else:
            assert False

    def num_requests(self):
        if self.__state == self.OIL:
            return self.__oil.num_requests()
        elif self.__state == self.OIL_FADE_OUT:
            return self.__wood.num_requests()
        elif self.__state == self.WOOD:
            return self.__wood.num_requests()
        elif self.__state == self.WOOD_FADE_OUT:
            return self.__wood.num_requests()
        else:
            assert False

    def print_requests(self):
        if self.__state == self.OIL:
            return self.__oil.print_requests()
        elif self.__state == self.OIL_FADE_OUT:
            return self.__wood.print_requests()
        elif self.__state == self.WOOD:
            return self.__wood.print_requests()
        elif self.__state == self.WOOD_FADE_OUT:
            return self.__wood.print_requests()
        else:
            assert False

    def is_requested_by(self, sink):
        if self.__state == self.OIL:
            return self.__oil.is_requested_by(sink)
        elif self.__state == self.OIL_FADE_OUT:
            return self.__wood.is_requested_by(sink)
        elif self.__state == self.WOOD:
            return self.__wood.is_requested_by(sink)
        elif self.__state == self.WOOD_FADE_OUT:
            return self.__wood.is_requested_by(sink)
        else:
            assert False

    def temperature(self):
        if self.__state == self.OIL:
            return self.__oil_temperature
        elif self.__state == self.OIL_FADE_OUT:
            return self.__oil_temperature
        elif self.__state == self.WOOD:
            return self.__wood_temperature
        elif self.__state == self.WOOD_FADE_OUT:
            return self.__wood_temperature
        else:
            assert False

    def __change_state(self, state, msg):
        self.__debug('%s -> %s (%s)' % (self.__state_str(self.__state), self.__state_str(state), msg))
        self.__state = state

    def __debug(self, msg):
        logging.debug('%s: %s' % (self.__name, msg))

    @staticmethod
    def __state_str(state):
        if state == OilWoodCombination.OIL:
            return 'OIL'
        elif state == OilWoodCombination.OIL_FADE_OUT:
            return 'OIL_FADE_OUT'
        elif state == OilWoodCombination.WOOD:
            return 'WOOD'
        elif state == OilWoodCombination.WOOD_FADE_OUT:
            return 'WOOD_FADE_OUT'
        else:
            assert False

