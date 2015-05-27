from .thinker import Thinker, CompositeThinker

from ..base import logger
from ..base.error import HeatingError

class Brain:
    class InfiniteLoop(HeatingError):
        pass
    class DuplicateThinker(HeatingError):
        pass

    def __init__(self, thinkers, max_loop=100):
        # sanity check: check for duplicates
        if True:
            seen = []
            for t in thinkers:
                t.visit_thinker(seen)
            unique_names = set()
            for name, obj in seen:
                if name in unique_names:
                    raise self.DuplicateThinker('duplicate thinker: %s (%s)' % (name, str(obj)))
                unique_names.add(name)

        self.__thinkers = thinkers

        # we count number of think() requests (for debugging/logging
        # only)
        self.__round = 0

        # infinite loop detection
        self.__max_loop = max_loop

    def think(self, message=''):
        thinkers_str = ','.join((t.name() for t in self.__thinkers))
        logger.debug('THINK ROUND #%d (%s), thinkers:%s' % (self.__round, message, thinkers_str))

        for t in self.__thinkers:
            t.init_thinking_local()

        for t in self.__thinkers:
            t.init_thinking_global()

        annotations_per_loop = []
        exc = None
        for loop in range(self.__max_loop):
            thoughts = []
            for t in self.__thinkers:
                local_thoughts = t.think()
                if True:
                    # paranoia
                    assert type(local_thoughts) in (list, tuple), t
                    for elem in local_thoughts:
                        assert type(elem) in (list, tuple)
                        assert len(elem) == 2
                thoughts.extend(local_thoughts)
            if len(thoughts) == 0:
                break
            annotations_per_loop.append((loop, thoughts))
        else:
            # check if somebody misbehaves. if so, we raise only after
            # the thinkers' finish_*() methods have been called
            exc = self.InfiniteLoop('infinite think loop detected')


        for t in self.__thinkers:
            t.finish_thinking_global()

        for t in self.__thinkers:
            t.finish_thinking_local()

        self.__round += 1

        if exc is not None:
            raise exc

        return annotations_per_loop
