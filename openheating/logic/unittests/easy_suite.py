from .brain_tests import suite as brain_suite
from .tendency_tests import suite as tendency_suite
from .scenario_request_with_temperature import suite as scenario_request_with_temperature_suite

from .sink_tests import suite as sink_suite
from .transport_tests import suite as transport_suite
from .thermometer_center_tests import suite as thermometer_center_suite
from .switch_center_tests import suite as switch_center_suite

from .oil_tests import suite as oil_suite
from .oil_wood_tests import suite as oil_wood_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(brain_suite)
suite.addTest(tendency_suite)
suite.addTest(sink_suite)
suite.addTest(transport_suite)
suite.addTest(thermometer_center_suite)
suite.addTest(switch_center_suite)
suite.addTest(oil_suite)
suite.addTest(oil_wood_suite)

# "scenarios" (complete temperatur sequences, concrete reations
# etc. go here)
suite.addTest(scenario_request_with_temperature_suite)
