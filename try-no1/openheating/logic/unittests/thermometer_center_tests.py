from openheating.testutils.test_thermometer import TestThermometer

from openheating.logic.thermometer_center import ThermometerCenter, ThermometerCenterThermometer
from openheating.base.error import HeatingError

import time
import unittest


class ThermometerCenterTest(unittest.TestCase):
    def test_lookup(self):
        th_center = ThermometerCenter({'one': TestThermometer(23.4), 'two': TestThermometer(34.5)})
        self.assertAlmostEqual(th_center.temperature('one'), 23.4)
        self.assertAlmostEqual(th_center.temperature('two'), 34.5)

    def test_all_names(self):
        th_center = ThermometerCenter({'one': TestThermometer(23.4), 'two': TestThermometer(34.5)})
        all_names = set(th_center.all_names())
        self.assertEqual(len(all_names), 2)
        self.assertIn('one', all_names)
        self.assertIn('two', all_names)

    def test_adapter_thermometer(self):
        th1 = TestThermometer(42)
        th2 = TestThermometer(666)
        th_center = ThermometerCenter({'one': th1, 'two': th2})

        th1_client = ThermometerCenterThermometer(center=th_center, name='one')
        th2_client = ThermometerCenterThermometer(center=th_center, name='two')

        self.assertAlmostEqual(th1_client.temperature(), 42)
        self.assertAlmostEqual(th2_client.temperature(), 666)
        

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerCenterTest)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
