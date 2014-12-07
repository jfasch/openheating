from abc import ABCMeta, abstractmethod

class Switch(metaclass=ABCMeta):
    @abstractmethod
    def set_state(self, value):
        assert False, 'abstract'
    def on(self):
        self.set_state(True)
    def off(self):
        self.set_state(False)
