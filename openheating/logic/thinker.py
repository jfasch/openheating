class Thinker:
    def __init__(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def init_thinking_local(self):
        '''called before a think round. cannot count on anything else being
        initialized, so take care that you remain standalone.
        '''
        pass

    def init_thinking_global(self):
        '''called before a think round. everybody's initialized locally
        (init_thinking_local() has been called on each participant),
        so it is safe to depend on others.
        '''
        pass

    def think(self):
        '''Return number of thoughts'''
        return 0

    def finish_thinking_global(self):
        return

    def finish_thinking_local(self):
        return

    def expand(self):
        return [self]

class CompositeThinker(Thinker):
    def __init__(self, name, thinkers):
        Thinker.__init__(self, name)
        self.__thinkers = thinkers

    def thinkers(self):
        return self.__thinkers

    def expand(self):
        expanded = []
        for t in self.__thinkers:
            expanded.extend(t.expand())
        return expanded

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
