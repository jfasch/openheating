from .thermometer_test import suite as thermometer_suite
from .temperature_profile_test import suite as temperature_profile_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(thermometer_suite)
suite.addTest(temperature_profile_suite)
