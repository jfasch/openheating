from ..control.thermometer import Thermometer

import os

class HWMON_Thermometer(Thermometer):
    def __init__(self, number):
        assert type(number) is int
        self.__temp_input = _input_file(number)
        if not os.path.isfile(self.__temp_input):
            raise HeatingException('HWMON thermometer: missing '+self.__temp_input)

    def temperature(self):
        temp = open(self.__temp_input, 'r').read()
        return int(temp)/1000

def iter_devices():
    for d in os.listdir(_HWMON_CLASS):
        if not d.startswith('hwmon'):
            continue
        number = int(d[5:])
        if not os.path.isfile(_input_file(number)):
            # obviously not a thermometer; skip
            continue
        yield number, HWMON_Thermometer(number)

_HWMON_CLASS = '/sys/class/hwmon'
_TEMP_INPUT = 'temp1_input'

def _input_file(number):
    return os.path.join(_HWMON_CLASS, 'hwmon%d' % number, _TEMP_INPUT)
