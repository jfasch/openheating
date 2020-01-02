from openheating.dbus import pyconf
from openheating.base.thermometer import FixedThermometer
from openheating.base.w1 import W1Thermometer
from openheating.test import testutils

import unittest
import tempfile


class ThermometerConfigTest(unittest.TestCase):
    def test__basic__pyconf(self):
        slist = [
            "from openheating.base.thermometer import FixedThermometer",
            "THERMOMETERS = [",
            "    FixedThermometer(name='Oil', description='From Hell with Decimal Points', temperature=666.666),",
            "    FixedThermometer(name='Wood', description='The Answer with Decimal Points', temperature=42.42),",
            "]",
        ]

        # read from line-list
        thermometers = pyconf.read_thermometers(
            slist, bus = None)
        self.__assert_basic__ok(thermometers)

        # read from str
        thermometers = pyconf.read_thermometers('\n'.join(slist), bus = None)
        self.__assert_basic__ok(thermometers)

        # read from file
        with tempfile.TemporaryFile() as f:
            f.write('\n'.join(slist).encode(encoding='ascii'))
            f.seek(0)
            self.__assert_basic__ok(pyconf.read_thermometers(f, bus = None))

    def __assert_basic__ok(self, thermometers):
        have_oil = have_wood = False
        for t in thermometers:
            if t.get_name() == 'Oil':
                self.assertTrue(isinstance(t, FixedThermometer))
                self.assertAlmostEqual(t.get_temperature(), 666.666)
                self.assertEqual(t.get_description(), 'From Hell with Decimal Points')
                have_oil = True
                continue

            if t.get_name() == 'Wood':
                self.assertTrue(isinstance(t, FixedThermometer))
                self.assertAlmostEqual(t.get_temperature(), 42.42)
                self.assertEqual(t.get_description(), 'The Answer with Decimal Points')
                have_wood = True
                continue

        self.assertTrue(have_oil)
        self.assertTrue(have_wood)

    def test__w1__pyconf(self):
        self.__assert_w1__ok(pyconf.read_thermometers(
            [
                "from openheating.base.w1 import W1Thermometer",
                "THERMOMETERS = [",
                "    W1Thermometer(",
                "        name='Oil',",
                "        description='Oil Burner',",
                "        path='/sys/bus/w1/devices/28-02131dace9aa'),",
                "    W1Thermometer(",
                "        name='Wood',",
                "        description='Wood Oven',",
                "        path='/sys/bus/w1/devices/28-02131dace9ab'),",
                "]",
            ],
            bus = None))

    def __assert_w1__ok(self, thermometers):
        have_oil = have_wood = False
        for t in thermometers:
            if t.get_name() == 'Oil':
                self.assertTrue(isinstance(t, W1Thermometer))
                self.assertEqual(t.get_name(), 'Oil')
                self.assertEqual(t.get_description(), 'Oil Burner')
                have_oil = True
                continue

            if t.get_name() == 'Wood':
                self.assertTrue(isinstance(t, W1Thermometer))
                self.assertEqual(t.get_name(), 'Wood')
                self.assertEqual(t.get_description(), 'Wood Oven')
                have_wood = True
                continue

        self.assertTrue(have_oil)
        self.assertTrue(have_wood)

    def test__bad_thermometer_name__pyconf(self):
        with self.assertRaises(pyconf.BadName) as what:
            pyconf.read_thermometers(
                [
                    "from openheating.base.thermometer import FixedThermometer",
                    "THERMOMETERS = [FixedThermometer(name='bad-name', description='blah', temperature=42)]",
                ], 
                bus = None)

        self.assertEqual(what.exception.name, 'bad-name')

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerConfigTest)

if __name__ == '__main__':
    testutils.run(suite)
