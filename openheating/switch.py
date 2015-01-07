from abc import ABCMeta, abstractmethod

class Switch(metaclass=ABCMeta):
    states = OPEN, CLOSED = 42, 666
    
    @abstractmethod
    def set_state(self, value):
        assert False, 'abstract'
    @abstractmethod
    def get_state(self):
        assert False, 'abstract'
        return self.CLOSED

    def do_close(self):
        self.set_state(self.CLOSED)
    def do_open(self):
        self.set_state(self.OPEN)
    def is_closed(self):
        return self.get_state() == self.CLOSED
    def is_open(self):
        return self.get_state() == self.OPEN
