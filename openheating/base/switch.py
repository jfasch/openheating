from abc import ABCMeta, abstractmethod


class Switch(metaclass=ABCMeta):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def set_state(self, value):
        assert type(value) is bool
        assert False, 'abstract'
    @abstractmethod
    def get_state(self):
        assert False, 'abstract'
        return False

class DummySwitch(Switch):
    def __init__(self, name, description, state):
        super().__init__(name, description)
        self.state = state

    def set_state(self, state):
        self.state = state
    def get_state(self):
        return self.state
