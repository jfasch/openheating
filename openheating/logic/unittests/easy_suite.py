from .tendency_tests import suite as tendency_suite
from .scenario_request_with_temperature import suite as scenario_request_with_temperature_suite

from .sink_tests import suite as sink_suite
from .transport_tests import suite as transport_suite
from .oil_tests import suite as oil_suite
from .thermometer_center_tests import suite as thermometer_center_suite
from .switch_center_tests import suite as switch_center_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(tendency_suite)
suite.addTest(sink_suite)
suite.addTest(transport_suite)
suite.addTest(oil_suite)
suite.addTest(thermometer_center_suite)
suite.addTest(switch_center_suite)

suite.addTest(scenario_request_with_temperature_suite)
