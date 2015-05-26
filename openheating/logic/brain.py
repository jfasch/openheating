from .thinker import Thinker, CompositeThinker

from ..base import logger
from ..base.error import HeatingError

class Brain:
    class InfiniteLoop(HeatingError):
        pass
    class DuplicateThinker(HeatingError):
        pass

    def __init__(self, thinkers, max_loop=100):
        # we count number of think() requests (for debugging/logging
        # only)
        self.__round = 0

        # infinite loop detection
        self.__max_loop = max_loop

        # sanity check: check for duplicates
        unique_names = set()
        for t in thinkers:
            expanded = t.expand()
            for e in expanded:
                if e.name() in unique_names:
                    raise self.DuplicateThinker('duplicate thinker: '+e.name()+'('+str(e)+')')
                unique_names.add(e.name())

        self.__thinkers = thinkers

    def think(self, message=''):
        thinkers_str = ','.join((t.name() for t in self.__thinkers))
        logger.debug('THINK ROUND #%d (%s), thinkers:%s' % (self.__round, message, thinkers_str))

        for t in self.__thinkers:
            t.init_thinking_local()

        for t in self.__thinkers:
            t.init_thinking_global()

        loop = 0
        exc = None
        while True:
            # check if somebody misbehaves. if so, we raise only after
            # the thinkers' finish_*() metods have been called
            if loop == self.__max_loop:
                exc = self.InfiniteLoop('infinite (%d) think loop detected' % loop)
                break
            loop += 1

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

        if exc is not None:
            raise exc
