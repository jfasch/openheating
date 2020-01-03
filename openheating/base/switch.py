from abc import ABCMeta, abstractmethod
import tempfile


class Switch(metaclass=ABCMeta):
    @abstractmethod
    def get_name(self):
        assert False, 'abstract'
        return 'name'

    @abstractmethod
    def get_description(self):
        assert False, 'abstract'
        return 'description'

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
        super().__init__()
        self.__name = name
        self.__description = description
        self.__state = state

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state
