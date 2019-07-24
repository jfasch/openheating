from abc import ABCMeta, abstractmethod


class Thermometer(metaclass=ABCMeta):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_temperature(self):
        assert False, 'abstract'
        return 23.4
