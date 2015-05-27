from abc import ABCMeta, abstractmethod

class Thinker(metaclass=ABCMeta):
    @abstractmethod
    def name(self):
        return 'some.name'

    @abstractmethod
    def visit_thinker(self, seen):
        '''debugging aid; augments seen with (name, object) tuples'''
        pass

    @abstractmethod
    def init_thinking_local(self):
        '''called before a think round. cannot count on anything else being
        initialized, so take care that you remain standalone.
        '''
        pass

    @abstractmethod
    def init_thinking_global(self):
        '''called before a think round. everybody's initialized locally
        (init_thinking_local() has been called on each participant),
        so it is safe to depend on others.
        '''
        pass

    @abstractmethod
    def think(self):
        '''Return number of thoughts'''
        return 0

    @abstractmethod
    def finish_thinking_global(self):
        return

    @abstractmethod
    def finish_thinking_local(self):
        return
        

class LeafThinker(Thinker):
    def __init__(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def visit_thinker(self, seen):
        seen.append((self.__name, self))

    def init_thinking_local(self):
        pass

    def init_thinking_global(self):
        pass

    def think(self):
        return 0

    def finish_thinking_global(self):
        return

    def finish_thinking_local(self):
        return

class CompositeThinker(Thinker):
    def __init__(self, name, thinkers):
        self.__name = name
        self.__thinkers = thinkers

    def name(self):
        return self.__name

    def visit_thinker(self, seen):
        for t in self.__thinkers:
            t.visit_thinker(seen)

    def init_thinking_local(self):
        for t in self.__thinkers:
            t.init_thinking_local()

    def init_thinking_global(self):
        for t in self.__thinkers:
            t.init_thinking_global()

    def think(self):
        num = 0
        for t in self.__thinkers:
            num += t.think()
        return num

    def finish_thinking_global(self):
        for t in self.__thinkers:
            t.finish_thinking_global()

    def finish_thinking_local(self):
        for t in self.__thinkers:
            t.finish_thinking_local()
