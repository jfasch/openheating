from abc import ABCMeta, abstractmethod

class Pump(metaclass=ABCMeta):
    @abstractmethod
    def is_running(self):
        assert False
        return False
    @abstractmethod
    def start(self):
        assert False
    @abstractmethod
    def stop(self):
        assert False
        
