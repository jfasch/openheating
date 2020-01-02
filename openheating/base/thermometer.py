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

class DummyThermometer(Thermometer):
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

class FixedThermometer(Thermometer):
    def __init__(self, name, description, temperature):
        super().__init__()
        self.__name = name
        self.__description = description
        self.__temperature = temperature

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_temperature(self):
        return self.__temperature


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

class FileThermometer(Thermometer):
    def __init__(self, name, description, path):
        self.__name = name
        self.__description = description
        self.__path = path

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_temperature(self):
        with open(self.__path) as f:
            return float(f.read())

    @classmethod
    def init_file(cls, temperature):
        tf = tempfile.NamedTemporaryFile(mode='w')
        tf.write(str(temperature))
        tf.flush()
        return tf
