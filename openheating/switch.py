from abc import ABCMeta, abstractmethod


class Switch(metaclass=ABCMeta):
    @abstractmethod
    def set_state(self, value):
        assert False, 'abstract'
    @abstractmethod
    def get_state(self):
        assert False, 'abstract'
        return False
