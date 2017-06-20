from abc import ABCMeta, abstractmethod
import datetime


class Thermometer(metaclass=ABCMeta):
    def get_temperature():
        assert False, 'abstract'
        return 23.4
