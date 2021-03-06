from .sink import Sink
from .thinker import Thinker

from ..base import logger

from abc import ABCMeta, abstractmethod


class Source(Thinker):
    def __init__(self, name):
        Thinker.__init__(self, name)
        self.__sinks = set()

    def add_sink(self, sink):
        assert sink not in self.__sinks
        self.__sinks.add(sink)
        sink.set_source(self)

    # jjj

    # @abstractmethod
    # def request(self, sink, temperature):
    #     pass

    # @abstractmethod
    # def num_requests(self):
    #     return 42

    # @abstractmethod
    # def print_requests(self):
    #     return '...'

    # @abstractmethod
    # def is_requested_by(self, sink):
    #     return True

    @abstractmethod
    def temperature(self):
        return 42.0


# class DirectSource(Source, LeafThinker):
#     '''One that knows a maximum available temperature, and can accept or
#     deny requests based upon that.

#     '''
#     def __init__(self, name, max_produced_temperature):
#         LeafThinker.__init__(self, name)

#         self.__max_produced_temperature = max_produced_temperature
#         self.__requests = TemperatureRequests()

#     def init_thinking_local(self):
#         self.__requests.clear()

#     def request(self, sink, temperature):
#         if temperature > self.__max_produced_temperature:
#             self.__debug('deny request for %.1f (can only do %.1f)' % (temperature, self.__max_produced_temperature))
#             return False
#         self.__debug('accepting request for %.1f (can do %.1f)' % (temperature, self.__max_produced_temperature))
#         self.__requests.add(sink, temperature)
#         return True

#     def num_requests(self):
#         return self.__requests.num_requests()

#     def print_requests(self):
#         return str(self.__requests)

#     def is_requested_by(self, sink):
#         return self.__requests.is_member(sink)

#     def __debug(self, msg):
#         logger.debug(self.name()+': '+msg)
