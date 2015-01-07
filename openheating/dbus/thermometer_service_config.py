from .service_config import DBusServiceConfig

from ..hardware.thermometer_hwmon import HWMON_I2C_Thermometer
from ..testutils.thermometer import TestThermometer

import os.path

class ThermometerServiceConfig(DBusServiceConfig):
    PARENT_PATH = 'PARENT_PATH'
    THERMOMETERS = 'THERMOMETERS'
    
    def __init__(self, content):
        DBusServiceConfig.__init__(
            self,
            symbols={
                'HWMON_I2C_Thermometer': HWMON_I2C_Thermometer,
                'TestThermometer': TestThermometer,
                },
            content=content)

        self.__parent_path = self.config().get('PARENT_PATH')
        thermometers = self.config().get('THERMOMETERS')

        if self.__parent_path is None:
            raise HeatingError('"PARENT_PATH" not specified')
        if thermometers is None:
            raise HeatingError('"THERMOMETERS" not specified')

        self.__thermometers = []
        for t in thermometers:
            self.__thermometers.append({'object_path': os.path.join(self.__parent_path, t[0]),
                                        'thermometer': t[1]})

    def thermometers(self):
        return self.__thermometers
