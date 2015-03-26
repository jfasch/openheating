from .sink import Sink
from .thinking import Thinker
from .request import TemperatureRequests
from . import logger

from abc import ABCMeta, abstractmethod


class Source(metaclass=ABCMeta):
    @abstractmethod
    def request(self, sink, temperature):
        pass

    @abstractmethod
    def num_requests(self):
        return 42

    @abstractmethod
    def print_requests(self):
        return '...'

    @abstractmethod
    def is_requested_by(self, sink):
        return True

    @abstractmethod
    def temperature(self):
        return 42.0


class DirectSource(Source, Thinker):
    '''One that knows a maximum available temperature, and can accept or
    deny requests based upon that.

    '''
    def __init__(self, name, max_produced_temperature):
        Thinker.__init__(self, name)

        self.__max_produced_temperature = max_produced_temperature
        self.__requests = TemperatureRequests()

    def register_thinking(self, brain):
        super().register_thinking(brain)
        brain.register_thinker(self)

    def init_thinking_local(self):
        self.__requests.clear()

    def request(self, sink, temperature):
        if temperature > self.__max_produced_temperature:
            self.__debug('deny request for %f (can only do %f)' % (temperature, self.__max_produced_temperature))
            return False
        self.__debug('accepting request for %f (can do %f)' % (temperature, self.__max_produced_temperature))
        self.__requests.add(sink, temperature)
        return True

    def num_requests(self):
        return self.__requests.num_requests()

    def print_requests(self):
        return str(self.__requests)

    def is_requested_by(self, sink):
        return self.__requests.is_member(sink)

    def __debug(self, msg):
        logger.debug(self.name()+': '+msg)
