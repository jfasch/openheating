from .thermometer_test import suite as thermometer_suite
from .thermometers_ini import suite as thermometers_ini_suite
from .thermometer_history import suite as thermometer_history_suite
from .switches_ini import suite as switches_ini_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(thermometer_suite)
suite.addTest(thermometers_ini_suite)
suite.addTest(thermometer_history_suite)
suite.addTest(switches_ini_suite)
