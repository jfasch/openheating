from abc import ABCMeta, abstractmethod

class Producer(metaclass=ABCMeta):
    def temperature(self):
        assert False, 'abstract'
        return 25.4
    pass
