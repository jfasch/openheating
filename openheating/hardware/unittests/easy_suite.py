from .sensors_tests import suite as sensors_suite
from .sensors_config_tests import suite as sensors_config_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(sensors_suite)
suite.addTest(sensors_config_suite)
