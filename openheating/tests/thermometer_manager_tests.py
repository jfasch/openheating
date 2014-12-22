from openheating.testutils.thermometer import TestThermometer

from openheating.thermometer_manager import ThermometerManager
from openheating.error import HeatingException

import time
import unittest

class ThermometerTest(unittest.TestCase):
    def test_lookup(self):
        th_man = ThermometerManager((('one', TestThermometer(23.4)), ('two', TestThermometer(34.5))))
        self.assertAlmostEqual(th_man.temperature('one'), 23.4)
        self.assertAlmostEqual(th_man.temperature('two'), 34.5)

    def test_duplicate(self):
        self.assertRaises(HeatingException, ThermometerManager, (('one', TestThermometer(23.4)), ('one', TestThermometer(34.5))) )

    def test_cache(self):
        th = TestThermometer(23.4)
        th_man = ThermometerManager((('one', th),), cache_age=0.2)
        self.assertEqual(th.num_calls(), 0)
        self.assertAlmostEqual(th_man.temperature('one'), 23.4)
        self.assertEqual(th.num_calls(), 1)
        self.assertAlmostEqual(th_man.temperature('one'), 23.4)
        self.assertEqual(th.num_calls(), 1)

        time.sleep(0.5)

        self.assertAlmostEqual(th_man.temperature('one'), 23.4)
        self.assertEqual(th.num_calls(), 2)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
