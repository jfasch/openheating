from .thermometer_hwmon import HWMON_I2C_Thermometer
from .testutils.thermometer import TestThermometer


class ConfigParser:
    def __init__(self, symbols):
        self.__symbols = symbols

    def parse(self, content):
        context = {}
        context.update(self.__symbols)
        exec(content, context)
        return context
