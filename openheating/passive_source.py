from .source import Source
from .thinking import Thinker

class PassiveSource(Source, Thinker):
    def __init__(self, name, max_produced_temperature, thermometer):
        Source.__init__(self, name=name, max_produced_temperature=max_produced_temperature)
        self.__thermometer = thermometer

    def temperature(self):
        return self.__thermometer.temperature()

    def think(self):
        return 0
    def sync(self):
        pass
