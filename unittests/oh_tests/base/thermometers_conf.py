from openheating import thermometers_conf
from openheating.thermometer import FixedThermometer
from openheating.w1 import W1Thermometer
from openheating.error import BadDBusPathComponent
from openheating.test import testutils

import unittest
import tempfile


class ThermometerConfigTest(unittest.TestCase):
    def test__basic__ini(self):
        thermometers = thermometers_conf.read_ini(
            """
            [Oil]
            Type = fixed
            Description = From Hell with Decimal Points
            Value = 666.666

            [Wood]
            Type = fixed
            Description = The Answer with Decimal Points
            Value = 42.42
            """
        )
        self.__assert_basic__ok(thermometers)

    def test__basic__pyconf(self):
        slist = [
            "from openheating.thermometer import FixedThermometer",
            "THERMOMETERS['Oil'] = FixedThermometer(name='Oil', description='From Hell with Decimal Points', temperature=666.666)",
            "THERMOMETERS['Wood'] = FixedThermometer(name='Wood', description='The Answer with Decimal Points', temperature=42.42)",
        ]

        thermometers = thermometers_conf.read_pyconf(slist)
        self.__assert_basic__ok(thermometers)

        thermometers = thermometers_conf.read_pyconf('\n'.join(slist))
        self.__assert_basic__ok(thermometers)

        with tempfile.TemporaryFile() as f:
            f.write('\n'.join(slist).encode(encoding='ascii'))
            f.seek(0)
            thermometers = thermometers_conf.read_pyconf(f)
            self.__assert_basic__ok(thermometers)

    def __assert_basic__ok(self, thermometers):
        oil = thermometers.get('Oil')
        self.assertIsNotNone(oil)
        self.assertTrue(isinstance(oil, FixedThermometer))
        self.assertAlmostEqual(oil.get_temperature(), 666.666)
        self.assertEqual(oil.name, 'Oil')
        self.assertEqual(oil.description, 'From Hell with Decimal Points')

        wood = thermometers.get('Wood')
        self.assertIsNotNone(wood)
        self.assertTrue(isinstance(wood, FixedThermometer))
        self.assertAlmostEqual(wood.get_temperature(), 42.42)
        self.assertEqual(wood.name, 'Wood')
        self.assertEqual(wood.description, 'The Answer with Decimal Points')

    def test__w1__ini(self):
        thermometers = thermometers_conf.read_ini(
            """
            [Oil]
            Type = w1
            Description = Oil Burner
            Path = /sys/bus/w1/devices/28-02131dace9aa

            [Wood]
            Type = w1
            Description = Wood Oven
            Path = /sys/bus/w1/devices/28-02131dace9ab
            """
        )
        self.__assert_w1__ok(thermometers)

    def test__w1__pyconf(self):
        thermometers = thermometers_conf.read_pyconf([
            "from openheating.w1 import W1Thermometer",
            "THERMOMETERS['Oil'] = W1Thermometer(",
            "    name='Oil',",
            "    description='Oil Burner',",
            "    path='/sys/bus/w1/devices/28-02131dace9aa')",
            "THERMOMETERS['Wood'] = W1Thermometer(",
            "    name='Wood',",
            "    description='Wood Oven',",
            "    path='/sys/bus/w1/devices/28-02131dace9ab')",
        ])
        self.__assert_w1__ok(thermometers)

    def __assert_w1__ok(self, thermometers):
        oil = thermometers.get('Oil')
        self.assertIsNotNone(oil)
        self.assertTrue(isinstance(oil, W1Thermometer))
        self.assertEqual(oil.name, 'Oil')
        self.assertEqual(oil.description, 'Oil Burner')

        wood = thermometers.get('Wood')
        self.assertIsNotNone(wood)
        self.assertTrue(isinstance(wood, W1Thermometer))
        self.assertEqual(wood.name, 'Wood')
        self.assertEqual(wood.description, 'Wood Oven')

    def test__bad_thermometer_name__ini(self):
        self.assertRaises(BadDBusPathComponent, thermometers_conf.read_ini,
            """
            [bad-name]
            Type = w1
            """)

    def test__bad_thermometer_name__pyconf(self):
        self.assertRaises(BadDBusPathComponent, thermometers_conf.read_pyconf,
                          ["from openheating.thermometer import FixedThermometer",
                           "THERMOMETERS['bad-name'] = FixedThermometer(name='blah', description='blah', temperature=42)",
                          ])

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerConfigTest)

if __name__ == '__main__':
    testutils.run(suite)
