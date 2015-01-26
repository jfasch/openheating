from abc import ABCMeta, abstractmethod

class Switch(metaclass=ABCMeta):
    @abstractmethod
    def set_state(self, value):
        assert False, 'abstract'
    @abstractmethod
    def get_state(self):
        assert False, 'abstract'
        return False

    def do_close(self):
        self.set_state(True)
    def do_open(self):
        self.set_state(False)
    def is_closed(self):
        return self.get_state()
    def is_open(self):
        return not self.get_state()
