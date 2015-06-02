from abc import ABCMeta, abstractmethod

class Looper:
    class Trigger(metaclass=ABCMeta):
        @abstractmethod
        def trigger(self):
            pass

    def __init__(self, brain, triggers):
        self.__brain = brain
        self.__triggers = triggers
        self.__num_loops = 0

    def num_loops(self):
        return self.__num_loops

    def loop(self):
        self.__brain.think()
        for t in self.__triggers:
            t.trigger()
        self.__num_loops += 1
