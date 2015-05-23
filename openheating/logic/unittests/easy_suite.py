from .tendency_tests import suite as tendency_suite
from .complicated_scenario_tests import suite as complicated_scenario_suite

from .sink_tests import suite as sink_suite
from .transport_tests import suite as transport_suite
from .oil_tests import suite as oil_suite
from .thermometer_center_tests import suite as thermometer_center_suite
from .switch_center_tests import suite as switch_center_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(tendency_suite)
suite.addTest(complicated_scenario_suite)
suite.addTest(sink_suite)
suite.addTest(transport_suite)
suite.addTest(oil_suite)
suite.addTest(thermometer_center_suite)
suite.addTest(switch_center_suite)
