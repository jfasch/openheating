from .thinker import Thinker

from ..base import logger


class Brain:
    def __init__(self):
        self.__thinkers = set()
        self.__round = 0

    def register_thinker(self, thinker):
        assert isinstance(thinker, Thinker)
        self.__thinkers.add(thinker)

    def think(self, message):
        thinkers_str = ','.join((t.name() for t in self.__thinkers))
        logger.debug('THINK ROUND #%d (%s), thinkers:%s' % (self.__round, message, thinkers_str))

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
            t.finish_thinking_global()
            
        for t in self.__thinkers:
            t.finish_thinking_local()
            
        self.__round += 1
