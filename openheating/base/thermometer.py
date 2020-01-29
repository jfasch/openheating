from .error import HeatingError

from abc import ABCMeta, abstractmethod


class Thermometer(metaclass=ABCMeta):
    @abstractmethod
    def get_temperature(self):
        assert False, 'abstract'
        return 23.4

class FileThermometer(Thermometer):
    'Thermometer that reads its temperature from a file'

    def __init__(self, path, initial_value=None):
        self.__path = path

        if initial_value is not None:
            try:
                with open(self.__path, 'x') as f:
                    f.write(str(initial_value)+'\n')
            except FileExistsError: pass

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
    def __init__(self, value):
        super().__init__()
        self.__value = value

    def get_temperature(self):
        return self.__value

    def set_temperature(self, value):
        self.__value = value

class ErrorThermometer(Thermometer):
    def __init__(self, n_ok_before_error):
        super().__init__()
        self.__n_ok_before_error = n_ok_before_error

    def get_temperature(self):
        if self.__n_ok_before_error > 0:
            self.__n_ok_before_error -= 1
            return 42
        raise HeatingError('bullshit temperature')

