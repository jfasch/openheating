from openheating.base.thermometer import Thermometer

import unittest


class ThermometerTest(unittest.TestCase):
    def test__basic(self):
        class SequenceThermometer(Thermometer):
            def __init__(self, sequence):
                self.__sequence = sequence
            def get_name(self): return 'name'
            def get_description(self): return 'description'
            def get_temperature(self):
                rv = self.__sequence[0]
                del self.__sequence[0]
                return rv

        th = SequenceThermometer([1,2,3])
        self.assertEqual(th.get_temperature(), 1)
        self.assertEqual(th.get_temperature(), 2)
        self.assertEqual(th.get_temperature(), 3)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerTest)
