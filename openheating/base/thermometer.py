from .error import HeatingError

from abc import ABCMeta, abstractmethod
import os.path
import logging


class Thermometer(metaclass=ABCMeta):
    @abstractmethod
    def get_temperature(self):
        assert False, 'abstract'
        return 23.4

class FileThermometer(Thermometer):
    'Thermometer that reads its temperature from a file'

    def __init__(self, path, initial_value=None):
        self.__path = path

        # file does not exist or is empty. write initial value.
        if not os.path.isfile(self.__path) or os.path.getsize(self.__path) == 0:
            with open(self.__path, 'w') as f:
                if initial_value is None:
                    raise HeatingError('{} does not exist and initial_value not given'.format(self.__path))
                logging.debug('{}: initializing thermometer with {}'.format(self.__path, initial_value))
                f.write(str(initial_value)+'\n')
        elif initial_value is not None:
            logging.debug('{}: already in place, not initializing (with {})'.format(self.__path, initial_value))

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

