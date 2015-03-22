from openheating.unittests.file_switch_tests import suite as file_switch_suite
from openheating.unittests.file_thermometer_tests import suite as file_thermometer_suite
from openheating.unittests.tendency_tests import suite as tendency_suite
from openheating.unittests.sink_tests import suite as sink_suite
from openheating.unittests.transport_tests import suite as transport_suite
from openheating.unittests.oil_tests import suite as oil_suite
from openheating.unittests.thermometer_center_tests import suite as thermometer_center_suite
from openheating.unittests.switch_center_tests import suite as switch_center_suite
from openheating.unittests.config_parser_tests import suite as config_parser_suite
from openheating.unittests.complicated_scenario_tests import suite as complicated_scenario_suite

from openheating.dbus.unittests.easy_suite import suite as dbus_suite
from openheating.hardware.unittests.easy_suite import suite as hardware_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(file_switch_suite)
suite.addTest(file_thermometer_suite)
suite.addTest(tendency_suite)
suite.addTest(sink_suite)
suite.addTest(transport_suite)
suite.addTest(oil_suite)
suite.addTest(thermometer_center_suite)
suite.addTest(switch_center_suite)
suite.addTest(config_parser_suite)
suite.addTest(complicated_scenario_suite)

suite.addTest(dbus_suite)
suite.addTest(hardware_suite)
