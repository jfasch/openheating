from .source import Source
from .thinker import Thinker, CompositeThinker
from .tendency import Tendency

from ..base import logger


class OilWoodCombination(Source, CompositeThinker):
    def __init__(self, name, oil, wood, valve_switch, wood_warm, wood_hot):
        self.__controller = _Controller(name=name+'.controller',
                                        oil=oil, wood=wood, valve_switch=valve_switch,
                                        wood_warm=wood_warm, wood_hot=wood_hot)
        CompositeThinker.__init__(self, name=name, thinkers=[self.__controller, oil, wood])

    def request(self, sink, temperature):
        return self.__controller.request(sink, temperature)

    def num_requests(self):
        return self.__controller.num_requests()

    def print_requests(self):
        return self.__controller.print_requests()

    def is_requested_by(self, sink):
        return self.__controller.is_requested_by(sink)

    def temperature(self):
        return self.__controller.temperature()


class _Controller(Source, Thinker):

    OIL, OIL_FADE_OUT, WOOD, WOOD_FADE_OUT = 0, 1, 2, 3

    def __init__(self, name, oil, wood, valve_switch, wood_warm, wood_hot):
        assert wood_hot.low() - wood_warm.high() >= 6

        Thinker.__init__(self, name)

        self.__oil = oil
        self.__wood = wood
        self.__wood_warm = wood_warm
        self.__wood_hot = wood_hot
        self.__valve_switch = valve_switch
        self.__wood_tendency = Tendency()
        self.__state = self.OIL

    def init_thinking_global(self):
        self.__wood_temperature = self.__wood.temperature()
        self.__oil_temperature = self.__oil.temperature()

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

    def finish_thinking_local(self):
        super().finish_thinking_local()

        if self.__state == self.OIL:
            self.__valve_switch.do_open()
        elif self.__state == self.OIL_FADE_OUT:
            self.__valve_switch.do_open()
        elif self.__state == self.WOOD:
            self.__valve_switch.do_close()
        elif self.__state == self.WOOD_FADE_OUT:
            # wood fading out. in other words, does not insist in
            # cooling anymore. I am allowed to choose whichever is
            # hotter.
            if self.__wood_temperature > self.__oil_temperature:
                self.__valve_switch.do_close()
            else:
                self.__valve_switch.do_open()
        else:
            assert False

        del self.__wood_temperature
        del self.__oil_temperature

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
            return self.__oil.temperature()
        elif self.__state == self.OIL_FADE_OUT:
            return self.__oil.temperature()
        elif self.__state == self.WOOD:
            return self.__wood.temperature()
        elif self.__state == self.WOOD_FADE_OUT:
            return self.__wood.temperature()
        else:
            assert False

    def __change_state(self, state, msg):
        self.__debug('%s -> %s (%s)' % (self.__state_str(self.__state), self.__state_str(state), msg))
        self.__state = state

    def __debug(self, msg):
        logger.debug('%s: %s' % (self.name(), msg))

    @staticmethod
    def __state_str(state):
        if state == _Controller.OIL:
            return 'OIL'
        elif state == _Controller.OIL_FADE_OUT:
            return 'OIL_FADE_OUT'
        elif state == _Controller.WOOD:
            return 'WOOD'
        elif state == _Controller.WOOD_FADE_OUT:
            return 'WOOD_FADE_OUT'
        else:
            assert False
