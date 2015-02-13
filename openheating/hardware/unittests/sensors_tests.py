from openheating.error import HeatingError
from openheating.hardware.thermometer_hwmon import HWMON_I2C_Thermometer

import unittest


class SensorsTest(unittest.TestCase):

    # there ought to more tests, but that's more work to make them
    # portable ('easy'). currently, we can only test for correct error
    # handling when bus number 666 does not exist (which will break as
    # soon as we run it on a machine with 667 buses :-)
    
    def test__bus_not_exist(self):
        try:
            HWMON_I2C_Thermometer(bus_number=666, address=0x48, driver='some_driver').temperature()
        except HeatingError as e:
            self.assertEqual(e.token(), 'bus-not-exist')
            pass

        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SensorsTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
