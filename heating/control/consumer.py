from abc import ABCMeta, abstractmethod

class Consumer(metaclass=ABCMeta):
    @abstractmethod
    def temperature(self):
        assert False, 'abstract'
        return 24.3
    @abstractmethod
    def wanted_temperature(self):
        assert False, 'abstract'
        return 55.9

