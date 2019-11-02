from .error import HeatingError

from abc import ABCMeta, abstractmethod


class Thermometer(metaclass=ABCMeta):
    @abstractmethod
    def get_name(self):
        assert False, 'abstract'
        return 'name'

    @abstractmethod
    def get_description(self):
        assert False, 'abstract'
        return 'description'

    @abstractmethod
    def get_temperature(self):
        assert False, 'abstract'
        return 23.4


class FixedThermometer(Thermometer):
    def __init__(self, name, description, temperature):
        super().__init__()
        self.name = name
        self.description = description
        self.temperature = temperature

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_temperature(self):
        return self.temperature


class ErrorThermometer(Thermometer):
    def __init__(self, name, description, n_ok_before_error):
        super().__init__()
        self.name = name
        self.description = description
        self.n_ok_before_error = n_ok_before_error

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_temperature(self):
        if self.n_ok_before_error > 0:
            self.n_ok_before_error -= 1
            return 42
        raise HeatingError('bullshit temperature')
