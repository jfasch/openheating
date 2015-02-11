from openheating.hardware.tests.sensors_tests import suite as sensors_suite
from openheating.hardware.tests.sensors_config_tests import suite as sensors_config_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(sensors_suite)
suite.addTest(sensors_config_suite)
