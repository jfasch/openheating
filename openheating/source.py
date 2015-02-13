from abc import ABCMeta, abstractmethod

from .transport import Transport

class Source(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name
        self.__requesters = set()

    def request(self, transport):
        assert isinstance(transport, Transport)
        if transport not in self.__requesters:
            self.__requesters.add(transport)
            self.do_request()

    def release(self, transport):
        self.__requesters.discard(transport)
        self.do_release()

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
