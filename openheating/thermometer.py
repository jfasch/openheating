from .error import HeatingError

from abc import ABCMeta, abstractmethod

class Thermometer(metaclass=ABCMeta):
    @abstractmethod
    def temperature(self):
        assert False, 'abstract'
        return 25.4

