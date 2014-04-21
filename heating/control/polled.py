from abc import ABCMeta, abstractmethod

class Polled(metaclass=ABCMeta):
    @abstractmethod
    def poll(self):
        return
