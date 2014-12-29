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

    def test_proxy_thermometer(self):
        th1 = TestThermometer(42)
        th2 = TestThermometer(666)
        th_man = ThermometerManager((('one', th1), ('two', th2)))

        th1_client = th_man.create_proxy_thermometer('one')
        th2_client = th_man.create_proxy_thermometer('two')

        self.assertAlmostEqual(th1_client.temperature(), 42)
        self.assertAlmostEqual(th2_client.temperature(), 666)
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
