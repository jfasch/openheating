from abc import ABCMeta, abstractmethod
import logging

class Polled(metaclass=ABCMeta):
    @abstractmethod
    def poll(self):
        return

class Poller:
    def __init__(self):
        self.__polled = set()
        self.__round = 0
    def add(self, polled):
        self.__polled.add(polled)
    def poll(self, msg=''):
        if len(msg):
            logging.debug('poll round #%d (%s)', self.__round, msg)
        else:
            logging.debug('poll round #%d', self.__round)

        for p in self.__polled:
            p.poll()            
        self.__round += 1
