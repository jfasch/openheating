from .thinker import Thinker
from .source import DirectSource


class PassiveSource(DirectSource):
    def __init__(self, name, max_produced_temperature, thermometer):
        DirectSource.__init__(self, name, max_produced_temperature)
        self.__thermometer = thermometer

    def temperature(self):
        return self.__temperature

    def init_thinking_local(self):
        super().init_thinking_local()
        self.__temperature = self.__thermometer.temperature()

    def finish_thinking_local(self):
        super().finish_thinking_local()
        del self.__temperature
