from abc import ABCMeta, abstractmethod


class Thermometer(metaclass=ABCMeta):
    def get_temperature(self):
        assert False, 'abstract'
        return 23.4
