from openheating.config import parse_config
from openheating.testutils.thermometer import TestThermometer
from openheating.thermometer_hwmon import HWMON_I2C_Thermometer

import unittest

class ConfigTest(unittest.TestCase):
    def test__all_names(self):
        content = '\n'.join(
            ['SOME_STRING = "blah"',
             'HWMON_I2C_THERMOMETER = HWMON_I2C_Thermometer(bus_number=1, address=0x42)',
             'TEST_THERMOMETER = TestThermometer(initial_temperature=42)',
             ])
        
        config = parse_config(content)

        self.assertEqual(config['SOME_STRING'], 'blah')
        self.assertTrue(isinstance(config['HWMON_I2C_THERMOMETER'], HWMON_I2C_Thermometer))
        self.assertTrue(isinstance(config['TEST_THERMOMETER'], TestThermometer))

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ConfigTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
