from abc import ABCMeta, abstractmethod

from .sink import Sink

class Source(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name
        self.__requesters = set()

    def request(self, sink):
        assert isinstance(sink, Sink)
        self.__requesters.add(sink)
        self.do_request()

    def release(self, sink):
        self.__requesters.discard(sink)
        self.do_release()

    def num_requesters(self):
        return len(self.__requesters)

    def requesters(self):
        return self.__requesters

    @abstractmethod
    def temperature(self):
        return 42.0

    @abstractmethod
    def do_request(self):
        pass

    @abstractmethod
    def do_release(self):
        pass
