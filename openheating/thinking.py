from abc import ABCMeta, abstractmethod
import logging

class Thinker(metaclass=ABCMeta):
    @abstractmethod
    def think(self):
        '''Return number of thoughts'''
        return 7
    @abstractmethod
    def sync(self):
        return

class Brain:
    def __init__(self):
        self.__thinkers = set()
        self.__round = 0

    def add(self, thinker):
        assert isinstance(thinker, Thinker)
        assert thinker not in self.__thinkers
        self.__thinkers.add(thinker)

    def think(self, msg=''):
        if len(msg):
            logging.debug('think round #%d (%s)', self.__round, msg)
        else:
            logging.debug('think round #%d', self.__round)

        while True:
            nthoughts = 0
            for t in self.__thinkers:
                nthoughts += t.think()
            if nthoughts == 0:
                break

        for t in self.__thinkers:
            t.sync()
            
        self.__round += 1

class ThinkingSwitch:
    '''A bridge that makes a switch think a bit

    Sometimes a "Thinker" makes decisions based on temperatures, and
    sets a switch accordingly (for example, a pump is switched on
    because source and sink temperatures differ sufficiently). Setting
    the switch not necessarily changes its state - the switch might
    have had that state before. Only when the state changes, this
    weighs in as a "thought".

    Consequentially a ThinkingSwitch encapsulates (has) a switch, and
    operates on it accordingly in the set() method.

    '''

    def __init__(self, switch):
        self.__switch = switch
        self.__state = None

    def set(self, state):
        '''Set the switch to state (a bool value)
        
        Returns > 0 if the switch state had to change (a
        decision/thought was made), and 0 otherwise.

        '''

        assert type(state) is bool
        
        if state != self.__state:
            self.__state = state
            return 1
        else:
            return 0

    def sync(self):
        if self.__state is not None:
            self.__switch.set_state(self.__state)

    def reset(self):
        self.__state = None
