from .file_switch_tests import suite as file_switch_suite
from .file_thermometer_tests import suite as file_thermometer_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(file_switch_suite)
suite.addTest(file_thermometer_suite)
