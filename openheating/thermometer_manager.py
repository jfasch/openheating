from .thermometer import Thermometer
from .error import HeatingException

from abc import ABCMeta, abstractmethod
import time

class ThermometerManagerBase(metaclass=ABCMeta):

    @abstractmethod
    def temperature(self, name):
        return 42.666

    def create_proxy_thermometer(self, name):
        return self._ProxyThermometer(manager=self, name=name)

    class _ProxyThermometer(Thermometer):
        def __init__(self, manager, name):
            self.__manager = manager
            self.__name = name
        def temperature(self):
            return self.__manager.temperature(self.__name)
    

class ThermometerManager(ThermometerManagerBase):
    def __init__(self, thermometers, cache_age=None):
        self.__thermometers = {}
        for name, th in thermometers:
            if name in self.__thermometers:
                raise HeatingException('duplicate thermometer "%s"' % name)
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
            raise HeatingException('no thermometer "%s"' % name)
        temp = th.temperature()
        if self.__cache_age is not None:
            self.__cache[name] = (temp, now)
        
        return temp
