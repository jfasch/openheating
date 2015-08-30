class Thinker:
    def __init__(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def visit_thinker(self, seen):
        '''debugging aid; augments seen with (name, object) tuples'''
        seen.append((self.__name, self))

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
        '''Return thoughts. [(name, thought_string), (name, thought_string), ...] '''
        return []

    def finish_thinking_global(self):
        pass

    def finish_thinking_local(self):
        pass
        

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
        thoughts = []
        for t in self.__thinkers:
            local_thoughts = t.think()
            if True:
                # paranoia
                assert type(local_thoughts) in (list, tuple), t
                for elem in local_thoughts:
                    assert type(elem) in (list, tuple), t
                    assert len(elem) == 2
            thoughts.extend(local_thoughts)
        return thoughts

    def finish_thinking_global(self):
        for t in self.__thinkers:
            t.finish_thinking_global()

    def finish_thinking_local(self):
        for t in self.__thinkers:
            t.finish_thinking_local()
