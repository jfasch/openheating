from abc import ABCMeta, abstractmethod
import logging

class Thinker(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def register_thinking(self, brain):
        assert isinstance(brain, Brain)

    def init_thinking_local(self):
        pass

    def init_thinking_global(self):
        pass

    def think(self):
        '''Return number of thoughts'''
        return 0

    def finish_thinking(self):
        return

class Brain:
    def __init__(self):
        self.__thinkers = set()
        self.__round = 0

    def register_thinker(self, thinker):
        assert isinstance(thinker, Thinker)
        self.__thinkers.add(thinker)

    def think(self, msg=''):
        if len(msg):
            thinkers_str = ','.join((t.name() for t in self.__thinkers))
            logging.debug('THINK ROUND #%d (%s), thinkers:%s' % (self.__round, msg, thinkers_str))
        else:
            logging.debug('THINK ROUND #%d', self.__round)

        for t in self.__thinkers:
            t.init_thinking_local()

        for t in self.__thinkers:
            t.init_thinking_global()

        while True:
            nthoughts = 0
            for t in self.__thinkers:
                nthoughts += t.think()
            if nthoughts == 0:
                break

        for t in self.__thinkers:
            t.finish_thinking()
            
        self.__round += 1
