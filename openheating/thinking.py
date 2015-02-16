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
    '''Operates on a switch. Returns >0 everytime a "set" operation
    modifies the current switch state, and 0 otherwise. 

    This reflects "thinking" because a "thought" is made on
    modification, and none otherwise.
    '''

    def __init__(self, switch):
        self.__state = None
        self.__switch = switch

    def set(self, state):
        assert type(state) is bool
        
        if state != self.__state:
            self.__state = state
            return 1
        else:
            return 0

    def sync(self):
        if self.__state is not None:
            self.__switch.set_state(self.__state)
