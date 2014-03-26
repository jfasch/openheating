from abc import ABCMeta, abstractmethod

class Producer(metaclass=ABCMeta):
    @abstractmethod
    def temperature(self):
        assert False, 'abstract'
        return 25.4
    @abstractmethod
    def peek(self):
        assert False, 'abstract'
    pass
