from .thermometer_hwmon import HWMON_I2C_Thermometer
from .testutils.thermometer import DummyThermometer
from .error import HeatingException

import os.path

class ThermometerDBusServiceConfigParser:
    def parse(self, content):
        context = {
            'DummyThermometer': DummyThermometer,
            'HWMON_I2C_Thermometer': HWMON_I2C_Thermometer,
        }
        exec(content, context)

        daemon_address = context.get('DAEMON_ADDRESS')
        bus_name = context.get('BUS_NAME')
        parent_path = context.get('PARENT_PATH')
        thermometers = context.get('THERMOMETERS')

        if daemon_address is None:
            raise HeatingException('"DAEMON_ADDRESS" not specified')
        if bus_name is None:
            raise HeatingException('"BUS_NAME" not specified')
        if parent_path is None:
            raise HeatingException('"PARENT_PATH" not specified')
        if thermometers is None:
            raise HeatingException('"THERMOMETERS" not specified')

        my_thermometers = []
        for t in thermometers:
            my_thermometers.append({'object_path': os.path.join(parent_path, t[0]),
                                    'thermometer': t[1]})

        return ThermometerDBusServiceConfig(
            daemon_address=daemon_address,
            bus_name=bus_name,
            thermometers=my_thermometers)
        
class ThermometerDBusServiceConfig:
    def __init__(self, daemon_address, bus_name, thermometers):
        self.__daemon_address = daemon_address
        self.__bus_name = bus_name
        self.__thermometers = thermometers

    def daemon_address(self):
        return self.__daemon_address
    def bus_name(self):
        return self.__bus_name
    def thermometers(self):
        return self.__thermometers
