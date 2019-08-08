from .error import HeatingError

from abc import ABCMeta, abstractmethod


class Thermometer(metaclass=ABCMeta):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def get_temperature(self):
        assert False, 'abstract'
        return 23.4


class FixedThermometer(Thermometer):
    def __init__(self, name, description, temperature):
        super().__init__(name, description)
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature


class ErrorThermometer(Thermometer):
    def __init__(self, name, description):
        super().__init__(name, description)

    def get_temperature(self):
        raise HeatingError('bullshit')
