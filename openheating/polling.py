from abc import ABCMeta, abstractmethod
import logging

class Polled(metaclass=ABCMeta):
    @abstractmethod
    def poll(self):
        return

class Poller:
    def __init__(self, num_polls):
        self.__polled = set()
        self.__round = 0
        self.__num_polls = num_polls
    def add(self, polled):
        assert polled not in self.__polled
        self.__polled.add(polled)
    def poll(self, msg=''):
        if len(msg):
            logging.debug('poll round #%d (%s)', self.__round, msg)
        else:
            logging.debug('poll round #%d', self.__round)

        for i in range(self.__num_polls):
            for p in self.__polled:
                p.poll()

        self.__round += 1
