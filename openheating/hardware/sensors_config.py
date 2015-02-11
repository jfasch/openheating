from .thermometer_hwmon import HWMON_I2C_Thermometer

from ..config_parser import ConfigParser


class SensorsConfig:
    def __init__(self, content):
        self.__creators = []

        parser = ConfigParser(symbols=_symbols.copy())
        config = parser.parse(content)

        self.__sensors = config.get('SENSORS')

        if self.__sensors is None:
            raise HeatingError('"SENSORS" not specified')
        if type(self.__sensors) not in (list, tuple):
            raise HeatingError('"SENSORS" must have list or tuple type (was %s)' % str(type(self.__sensors)))

    def sensors(self):
        return self.__sensors

_symbols = {
    'HWMON_I2C_Thermometer': HWMON_I2C_Thermometer,
}
