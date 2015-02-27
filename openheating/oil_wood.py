from .source import Source
from .thinking import Thinker

import logging


class OilWoodCombination(Source, Thinker):

    OIL, OIL_FADE_OUT, WOOD, WOOD_FADE_OUT = 0, 1, 2, 3

    def __init__(self, name, oil, wood, valve_switch, wood_warm, wood_hot):
        assert wood_hot.low() - wood_warm.high() >= 10

        self.__name = name
        self.__oil = oil
        self.__wood = wood
        self.__wood_warm = wood_warm
        self.__wood_hot = wood_hot
        self.__valve_switch = valve_switch
        self.__wood_tendency = Tendency()

    def start_thinking(self):
        self.__oil_temperature = self.__oil.temperature()
        self.__wood_temperature = self.__wood.temperature()

        self.__wood_tendency.add(wood_temperature)

        # between either of the hysteresis ranges. undecided; state
        # left as-is, but do some debug output
        if self.__wood_warm.between(self.__wood_temperature):
            self.__debug('within wood-warm hysteresis range')
            return
        elif self.__wood_hot.between(self.__wood_temperature):
            self.__debug('within wood-hot hysteresis range')
            return

        # wood above hot -> clearly wood
        elif self.__wood_hot.above(self.__wood_temperature):
            self.__debug('wood is hot')
            self.__state = self.WOOD
            return
        # wood below warm -> clearly oil
        elif self.__wood_warm.below(self.__wood_temperature):
            self.__debug('wood is cold')
            self.__state = self.OIL
            return

        # wood between warm and hot; let tendency rule
        elif self.__wood_tendency.rising():
            self.__debug('warm/hot, rising')
            self.__state = self.OIL_FADE_OUT
            return
        elif self.__wood_tendency.falling():
            self.__debug('warm/hot, falling')
            self.__state = self.WOOD_FADE_OUT
            return
        else:
            # no tendency, leave state as-is
            self.__debug('fading, but no tendency')

    def stop_thinking(self):
        del self.__wood_temperature
        del self.__oil_temperature

        if self.__state == self.OIL:
            self.__valve_switch.do_open()
            return
        if self.__state == self.OIL_FADE_OUT:
            self.__valve_switch.do_open()
            return
        if self.__state == self.WOOD:
            self.__valve_switch.do_close()
            return
        if self.__state == self.WOOD_FADE_OUT:
            self.__valve_switch.do_close()
            return
        assert False
            
    def temperature(self):
        if self.__state == self.OIL:
            return self.__oil_temperature
        if self.__state == self.OIL_FADE_OUT:
            return self.__oil_temperature
        if self.__state == self.WOOD:
            return self.__wood_temperature
        if self.__state == self.WOOD_FADE_OUT:
            return self.__wood_temperature
        assert False

    def think(self):
        # me not thinking, me only delegating
        return 0

    def __debug(self, msg):
        logging.debug('%s: %s (%s)' % (self.__name, msg, self.__state_str()))

    def __state_str(self):
        if self.__state == self.OIL:
            return 'OIL'
        if self.__state == self.OIL_FADE_OUT:
            return 'OIL_FADE_OUT'
        if self.__state == self.WOOD:
            return 'WOOD'
        if self.__state == self.WOOD_FADE_OUT:
            return 'WOOD_FADE_OUT'
        assert False

