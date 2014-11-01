from openheating.thermometer_manager import ThermometerManager
from openheating.error import HeatingException
from openheating.thermometer_dummy import DummyThermometer

import unittest

class ThermometerTest(unittest.TestCase):
    def test_lookup(self):
        th_man = ThermometerManager((('one', DummyThermometer(23.4)), ('two', DummyThermometer(34.5))))
        self.assertAlmostEqual(th_man.temperature('one'), 23.4)
        self.assertAlmostEqual(th_man.temperature('two'), 34.5)

    def test_duplicate(self):
        self.assertRaises(HeatingException, ThermometerManager, (('one', DummyThermometer(23.4)), ('one', DummyThermometer(34.5))) )

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerTest))

#suite.addTest(BurnerTest("test"))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
