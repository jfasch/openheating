from openheating.testutils.file_thermometer import FileThermometer
from openheating.testutils.persistent_test import PersistentTestCase

import unittest
import logging

class FileThermometerTest(PersistentTestCase):
    def test__basic(self):
        thermometer_path = self.rootpath()+'/thermometer'
        open(thermometer_path, 'w').write('0.5\n')
        thermometer= FileThermometer(path=thermometer_path)
        
        self.assertAlmostEqual(thermometer.temperature(), 0.5)

        open(thermometer_path, 'w').write('42.666\n')
        self.assertAlmostEqual(thermometer.temperature(), 42.666)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FileThermometerTest))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    runner = unittest.TextTestRunner()
    runner.run(suite)
