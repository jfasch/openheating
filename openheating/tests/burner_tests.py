from openheating.thermometer_dummy import DummyThermometer
from openheating.tests.switches import TestSwitch

from openheating.wolf_burner import WolfBurner

import unittest

class BurnerTest(unittest.TestCase):
    def test(self):
        thermometer = DummyThermometer(initial_temperature=20)
        inhibit_switch = TestSwitch(on=True)
        burn_switch = TestSwitch(on=False)
        burner = WolfBurner(inhibit_switch=inhibit_switch,
                            burn_switch=burn_switch,
                            thermometer=thermometer)

        # burner itself does not touch inhibit switch
        self.failUnless(inhibit_switch.is_on())
        self.failIf(burn_switch.is_on())

        burner.acquire()

        self.failUnless(inhibit_switch.is_on())
        self.failUnless(burn_switch.is_on())

        burner.release()

        self.failUnless(inhibit_switch.is_on())
        self.failIf(burn_switch.is_on())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BurnerTest))

#suite.addTest(BurnerTest("test"))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)