from ..logic.thermometer import Thermometer
from ..base.error import HeatingError

import os
import time


_HWMON_CLASS = '/sys/class/hwmon'
_TEMP_INPUT = 'temp1_input'

class HWMON_Thermometer(Thermometer):
    def __init__(self, number):
        assert type(number) is int
        self.__temp_input = _input_file(number)
        if not os.path.isfile(self.__temp_input):
            raise HeatingError('HWMON thermometer: missing '+self.__temp_input)

    def temperature(self):
        try:
            tempfile = open(self.__temp_input, 'r')
        except FileNotFoundError as e:
            # fixme: mark this as permanent
            raise HeatingError(msg=self.__temp_input+' not there', nested_errors=e)

        try:
            temp = tempfile.read()
        except IOError as e:
            raise HeatingError(msg='error reading '+self.__temp_input)

        return int(temp)/1000

class HWMON_I2C_Thermometer(HWMON_Thermometer):
    def __init__(self, bus_number, address, driver=None):
        assert type(bus_number) is int
        assert driver is None or type(driver) is str
        assert type(address) is int

        self.__bus_number = bus_number
        self.__driver = driver
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

        adapter_path = '/sys/class/i2c-adapter/i2c-%d' % self.__bus_number
        device_dir = '%d-%04x' % (self.__bus_number, self.__address)
        device_path = adapter_path + '/' + device_dir

        if not os.path.isdir(adapter_path):
            raise HeatingError(
                msg='No such adapter: '+adapter_path,
                permanent=True,
                token='bus-not-exist')
        
        if not os.path.isdir(device_path):
            # "hotplug" device if not yet in place, if we know the
            # driver.
            if self.__driver is None:
                raise HeatingError(
                    msg='HWMON I2C Thermometer: no such device: '+device_path,
                    permanent=True)
            try:
                with open(adapter_path + '/new_device', 'w') as new_device:
                    new_device.write('%s %s' % (self.__driver, self.__address))

                # writing to new_device does not create the device
                # (and all that it entails)
                # immediately. apparently. wait for the device to
                # appear.
                _wait_for_path(device_path)
            except OSError as e:
                raise HeatingError(
                    msg='Cannot add device "%s 0x%x" to adapter %s' % (self.__driver, self.__address, adapter_path),
                    permanent=True)
            except HeatingError as e:
                raise HeatingError(
                    msg='Cannot add device "%s 0x%x" to adapter %s' % (self.__driver, self.__address, adapter_path),
                    permanent=True,
                    nested_errors=[e])

        device_hwmon_path = os.path.join(device_path, 'hwmon')
        try:
            _wait_for_path(device_hwmon_path)
        except HeatingError as e:
            raise HeatingError(
                msg='HWMON I2C Thermometer: not a hwmon device; missing '+device_hwmon_path,
                permanent=True,
                nested_errors=[e])

        hwmon_devices = os.listdir(device_hwmon_path)
        if len(hwmon_devices) == 0:
            raise HeatingError(
                msg='HWMON I2C Thermometer: no device found in '+device_hwmon_path,
                permanent=True)

        if len(hwmon_devices) != 1:
            raise HeatingError(
                msg='HWMON I2C Thermometer: not implemented: found multiple (%d) devices in %s' % \
                    (len(hwmon_devices), device_hwmon_path),
                permanent=True)

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

def _wait_for_path(path, num=1000, interval=0.1):
    remain = num
    while not os.path.exists(path):
        if remain == 0:
            raise HeatingError(path+' does not exist after '+str(num*interval)+' seconds')
        time.sleep(interval)
        remain -= 1
