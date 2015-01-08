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
