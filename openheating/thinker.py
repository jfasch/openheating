class Thinker:
    def __init__(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def register_thinking(self, brain):
        pass
        
    def init_thinking_local(self):
        pass

    def init_thinking_global(self):
        pass

    def think(self):
        '''Return number of thoughts'''
        return 0

    def finish_thinking_global(self):
        return

    def finish_thinking_local(self):
        return

