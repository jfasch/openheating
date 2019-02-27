import openheating.thermometers_ini
from openheating.thermometer_fixed import FixedThermometer

import unittest
import io


class ThermometerIniTest(unittest.TestCase):
    def test__basic(self):
        thermometers = openheating.thermometers_ini.read(io.StringIO(
            """
            [Oil]
            Type = fixed
            Value = 666.666

            [Wood]
            Type = fixed
            Value = 42.42
            """
        ))

        oil = thermometers.get('Oil')
        self.assertIsNotNone(oil)
        self.assertTrue(isinstance(oil, FixedThermometer))
        self.assertAlmostEqual(oil.get_temperature(), 666.666)

        wood = thermometers.get('Wood')
        self.assertIsNotNone(wood)
        self.assertTrue(isinstance(wood, FixedThermometer))
        self.assertAlmostEqual(wood.get_temperature(), 42.42)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerIniTest)
