from .thermometer import Thermometer
from .error import HeatingError

from abc import ABCMeta, abstractmethod
import time

class ThermometerCenterBase(metaclass=ABCMeta):

    @abstractmethod
    def all_names(self):
        return ['blah']

    @abstractmethod
    def temperature(self, name):
        return 42.666

class ThermometerCenter(ThermometerCenterBase):
    def __init__(self, thermometers):
        assert type(thermometers) is dict
        self.__thermometers = thermometers

    def all_names(self):
        return self.__thermometers.keys()

    def temperature(self, name):
        th = self.__thermometers.get(name)
        if th is None:
            raise HeatingError('no thermometer "%s"' % name)
        return th.temperature()

    def num_thermometers__test(self):
        '''For tests only'''
        return len(self.__thermometers)
        
    def get_thermometer__test(self, name):
        '''For tests only'''
        return self.__thermometers.get(name)

class ThermometerCenterThermometer(Thermometer):
    '''Is-a Thermometer which uses a ThermometerCenter and a name to get
    to the temperature.'''

    def __init__(self, center, name):
        self.__center = center
        self.__name = name
    def temperature(self):
        return self.__center.temperature(self.__name)
