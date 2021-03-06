from .history import suite as history_suite
from .thermometer_test import suite as thermometer_suite
from .hysteresis import suite as hysteresis_suite
from .circuit import suite as circuit_suite
from .scenario_buffer_wants_heat import suite as scenario_buffer_wants_heat_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(history_suite)
suite.addTest(thermometer_suite)
suite.addTest(hysteresis_suite)
suite.addTest(circuit_suite)
suite.addTest(scenario_buffer_wants_heat_suite)
