from .thinking import Thinker
from .source import DirectSource


class PassiveSource(DirectSource):
    def __init__(self, name, max_produced_temperature, thermometer):
        DirectSource.__init__(self, name, max_produced_temperature)
        self.__thermometer = thermometer

    def temperature(self):
        return self.__thermometer.temperature()

    def think(self):
        return 0
