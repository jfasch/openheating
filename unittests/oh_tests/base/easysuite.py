from .history import suite as history_suite
from .thermometer_test import suite as thermometer_suite
from .thermometers_pyconf import suite as thermometers_pyconf_suite
from .switches_pyconf import suite as switches_pyconf_suite
from .hysteresis import suite as hysteresis_suite
from .circuit import suite as circuit_suite
from .heat_wanted import suite as heat_wanted_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(history_suite)
suite.addTest(thermometer_suite)
suite.addTest(thermometers_pyconf_suite)
suite.addTest(switches_pyconf_suite)
suite.addTest(hysteresis_suite)
suite.addTest(circuit_suite)
suite.addTest(heat_wanted_suite)
