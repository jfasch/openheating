from .error import HeatingError

from abc import ABCMeta, abstractmethod
import tempfile


class Thermometer(metaclass=ABCMeta):
    @abstractmethod
    def get_name(self):
        assert False, 'abstract'
        return 'name'

    @abstractmethod
    def get_description(self):
        assert False, 'abstract'
        return 'description'

    @abstractmethod
    def get_temperature(self):
        assert False, 'abstract'
        return 23.4

class FileThermometer(Thermometer):
    'Thermometer that reads its temperature from a file'

    def __init__(self, name, description, path, initial_value=None):
        self.__name = name
        self.__description = description
        self.__path = path

        if initial_value is not None:
            with open(self.__path, 'w') as f:
                f.write(str(initial_value)+'\n')

    def get_name(self):
        return self.__name
    def get_description(self):
        return self.__description
    def get_temperature(self):
        with open(self.__path) as f:
            return float(f.read())

    def set_temperature(self, value):
        '''not a Thermometer interface method. writes value to the backing file.'''
        # better error out early than late
        assert type(value) in (int, float)
        with open(self.__path, 'w') as f:
            f.write(str(value))

class InMemoryThermometer(Thermometer):
    def __init__(self, name, description, value):
        super().__init__()
        self.__name = name
        self.__description = description
        self.__value = value

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_temperature(self):
        return self.__value

    def set_temperature(self, value):
        self.__value = value

class ErrorThermometer(Thermometer):
    def __init__(self, name, description, n_ok_before_error):
        super().__init__()
        self.__name = name
        self.__description = description
        self.__n_ok_before_error = n_ok_before_error

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_temperature(self):
        if self.__n_ok_before_error > 0:
            self.__n_ok_before_error -= 1
            return 42
        raise HeatingError('bullshit temperature')

