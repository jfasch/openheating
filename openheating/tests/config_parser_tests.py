from openheating.config_parser import ConfigParser
from openheating.testutils.thermometer import TestThermometer
from openheating.thermometer_hwmon import HWMON_I2C_Thermometer

import unittest

class ConfigParserTest(unittest.TestCase):
    def test__basic(self):
        class SomeClass: pass

        parsed = ConfigParser(symbols={'MySomeClass': SomeClass}).parse(
            '\n'.join(
                ['SOME_STRING = "blah"',
                 'SOME_OBJECT = MySomeClass()',
             ]))

        self.assertEqual(parsed['SOME_STRING'], 'blah')
        self.assertIsInstance(parsed['SOME_OBJECT'], SomeClass)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ConfigParserTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
