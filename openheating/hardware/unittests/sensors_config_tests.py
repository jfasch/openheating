from openheating.hardware.sensors_config import SensorsConfig
from openheating.hardware.thermometer_hwmon import HWMON_I2C_Thermometer

import unittest


class SensorsConfigTest(unittest.TestCase):

    def test__sensors_from_config(self):
        config = SensorsConfig(_config)
        self.assertEqual(len(config.sensors()), 1)
        self.assertIsInstance(config.sensors()[0], HWMON_I2C_Thermometer)

_config = '''
SENSORS = (
    HWMON_I2C_Thermometer(bus_number=666, address=0x4a, driver='lm73'),
)
'''

        
suite = unittest.defaultTestLoader.loadTestsFromTestCase(SensorsConfigTest)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
