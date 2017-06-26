from openheating.core.thermometer import Thermometer
from openheating.core.temperature_profile import TemperatureProfile

import datetime
import unittest

class TemperatureProfileTest(unittest.TestCase):

    class MyThermometer(Thermometer):
        def __init__(self, temperatures):
            self.__temperatures = iter(temperatures)
        def get_temperature(self):
            return next(self.__temperatures)

    
    def test__basic(self):
        profile = TemperatureProfile(self.MyThermometer([10.1, 10.2, 10.3]))
        profile.pull_sample(datetime.datetime(1966, 6, 19, 1, 2, 0))
        profile.pull_sample(datetime.datetime(1966, 6, 19, 1, 2, 1))
        profile.pull_sample(datetime.datetime(1966, 6, 19, 1, 2, 2))

        sample_id, timestamp, temperature = profile.get_samples()[0]
        self.assertEqual(sample_id, 0)
        self.assertEqual(timestamp.year, 1966)
        self.assertEqual(timestamp.month, 6)
        self.assertEqual(timestamp.day, 19)
        self.assertEqual(timestamp.hour, 1)
        self.assertEqual(timestamp.minute, 2)
        self.assertEqual(timestamp.second, 0)

        sample_id, timestamp, temperature = profile.get_samples()[1]
        self.assertEqual(sample_id, 1)
        self.assertEqual(timestamp.year, 1966)
        self.assertEqual(timestamp.month, 6)
        self.assertEqual(timestamp.day, 19)
        self.assertEqual(timestamp.hour, 1)
        self.assertEqual(timestamp.minute, 2)
        self.assertEqual(timestamp.second, 1)

        sample_id, timestamp, temperature = profile.get_samples()[2]
        self.assertEqual(sample_id, 2)
        self.assertEqual(timestamp.year, 1966)
        self.assertEqual(timestamp.month, 6)
        self.assertEqual(timestamp.day, 19)
        self.assertEqual(timestamp.hour, 1)
        self.assertEqual(timestamp.minute, 2)
        self.assertEqual(timestamp.second, 2)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TemperatureProfileTest)
