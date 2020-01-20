from abc import ABCMeta, abstractmethod
import tempfile


class Switch(metaclass=ABCMeta):
    @abstractmethod
    def set_state(self, value):
        assert type(value) is bool
        assert False, 'abstract'

    @abstractmethod
    def get_state(self):
        assert False, 'abstract'
        return False

class FileSwitch(Switch):
    def __init__(self, path, initial_value=None):
        self.__path = path

        if initial_value is not None:
            with open(self.__path, 'w') as f:
                f.write(str(initial_value)+'\n')

    def set_state(self, value):
        with open(self.__path, 'w') as f:
            f.write(str(value)+'\n')
    def get_state(self):
        with open(self.__path) as f:
            return bool(eval(f.read()))

class InMemorySwitch(Switch):
    def __init__(self, state):
        super().__init__()
        self.__state = state

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state
