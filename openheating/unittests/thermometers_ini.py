from openheating.thermometers_ini import read_string
from openheating.thermometer_fixed import FixedThermometer
from openheating.w1 import W1Thermometer
from openheating.error import BadDBusPathComponent

import unittest


class ThermometerIniTest(unittest.TestCase):
    def test__basic(self):
        thermometers = read_string(
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

    def test_w1(self):
        thermometers = read_string(
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

    def test_bad_thermometer_name(self):
        self.assertRaises(BadDBusPathComponent, read_string,
            """
            [bad-name]
            Type = w1
            """)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerIniTest)
