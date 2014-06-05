from .thermometer import Thermometer
from .error import HeatingException

class ThermometerManager:
    def __init__(self, thermometers):
        self.__thermometers = {}
        for iD, th in thermometers:
            if iD in self.__thermometers:
                raise HeatingException('duplicate thermometer "%s"' % iD)
            self.__thermometers[iD] = th

    def temperature(self, iD):
        th = self.__thermometers.get(iD)
        if th is None:
            raise('no thermometer with ID '+iD)
        return th.temperature()
