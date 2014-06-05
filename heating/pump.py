from abc import ABCMeta, abstractmethod

class Pump(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        assert False
    @abstractmethod
    def stop(self):
        assert False
        
