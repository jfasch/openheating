from .thermometer import Thermometer
from .error import HeatingError

import os

_HWMON_CLASS = '/sys/class/hwmon'
_TEMP_INPUT = 'temp1_input'

class HWMON_Thermometer(Thermometer):
    def __init__(self, number):
        assert type(number) is int
        self.__temp_input = _input_file(number)
        if not os.path.isfile(self.__temp_input):
            raise HeatingError('HWMON thermometer: missing '+self.__temp_input)

    def temperature(self):
        temp = open(self.__temp_input, 'r').read()
        return int(temp)/1000

class HWMON_I2C_Thermometer(HWMON_Thermometer):
    def __init__(self, bus_number, address):
        self.__bus_number = bus_number
        self.__address = address
        self.__initialized = False
        pass

    def bus_number(self):
        return self.__bus_number
    def address(self):
        return self.__address

    def temperature(self):
        self.__lazy_init()
        return HWMON_Thermometer.temperature(self)

    def __lazy_init(self):
        if self.__initialized:
            return
        device_dir = '/sys/bus/i2c/devices/i2c-%d/%d-%04x' % (self.__bus_number, self.__bus_number, self.__address)
        if not os.path.isdir(device_dir):
            raise HeatingError('HWMON I2C Thermometer: no such device: '+device_dir)
        device_hwmon_dir = os.path.join(device_dir, 'hwmon')
        if not os.path.isdir(device_dir):
            raise HeatingError('HWMON I2C Thermometer: not a hwmon device; missing '+device_hwmon_dir)
        hwmon_devices = os.listdir(device_hwmon_dir)
        if len(hwmon_devices) == 0:
            raise HeatingError('HWMON I2C Thermometer: no device found in '+device_hwmon_dir)
        if len(hwmon_devices) != 1:
            raise HeatingError('HWMON I2C Thermometer: not implemented: found multiple (%d) devices in %s' % \
                                       (len(hwmon_devices), device_hwmon_dir))
        number = int(hwmon_devices[0][5:])
        HWMON_Thermometer.__init__(self, number)
        self.__initialized = True

def iter_devices():
    for d in os.listdir(_HWMON_CLASS):
        if not d.startswith('hwmon'):
            continue
        number = int(d[5:])
        if not os.path.isfile(_input_file(number)):
            # obviously not a thermometer; skip
            continue
        yield number, HWMON_Thermometer(number)

def _input_file(number):
    return os.path.join(_HWMON_CLASS, 'hwmon%d' % number, _TEMP_INPUT)
