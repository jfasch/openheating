from abc import ABCMeta, abstractmethod

from .sink import Sink

class Source(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name
        self.__requesters = set()

    def request(self, sink):
        assert isinstance(sink, Sink)
        self.__requesters.add(sink)

    def release(self, sink):
        self.__requesters.discard(sink)

    def num_requesters(self):
        return len(self.__requesters)

    def requesters(self):
        return self.__requesters

    @abstractmethod
    def temperature(self):
        return 42.0
