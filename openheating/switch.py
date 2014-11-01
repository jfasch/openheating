from abc import ABCMeta, abstractmethod

class Switch(metaclass=ABCMeta):
    @abstractmethod
    def on(self):
        assert False, 'abstract'
    def off(self):
        assert False, 'abstract'
