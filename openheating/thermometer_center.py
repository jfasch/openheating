from .thermometer import Thermometer
from .error import HeatingError

from abc import ABCMeta, abstractmethod
import time

class ThermometerCenterBase(metaclass=ABCMeta):

    @abstractmethod
    def temperature(self, name):
        return 42.666

    def get_thermometer(self, name):
        '''Returns an adapter onto self. The returned Thermometer, asked for its
        temperature, asks self by name
        '''
        return self._Adapter(center=self, name=name)

    class _Adapter(Thermometer):
        def __init__(self, center, name):
            self.__center = center
            self.__name = name
        def temperature(self):
            return self.__center.temperature(self.__name)
    

class ThermometerCenter(ThermometerCenterBase):
    def __init__(self, thermometers, cache_age=None):
        self.__thermometers = {}
        for name, th in thermometers:
            if name in self.__thermometers:
                raise HeatingError('duplicate thermometer "%s"' % name)
            self.__thermometers[name] = th

        self.__cache_age = cache_age
        if self.__cache_age is not None:
            self.__cache = {}

    def temperature(self, name):
        if self.__cache_age is not None:
            now = time.time()
            entry = self.__cache.get(name)
            if entry is not None and now - entry[1] < self.__cache_age:
                return entry[0]
        
        th = self.__thermometers.get(name)
        if th is None:
            raise HeatingError('no thermometer "%s"' % name)
        temp = th.temperature()
        if self.__cache_age is not None:
            self.__cache[name] = (temp, now)
        
        return temp
