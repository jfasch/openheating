from openheating.tests.sink_tests import suite as sink_suite
from openheating.tests.transport_tests import suite as transport_suite
from openheating.tests.oil_combo_tests import suite as oil_combo_suite
#from .burner_tests import suite as burner_suite
from openheating.tests.thermometer_center_tests import suite as thermometer_center_suite
from openheating.tests.switch_center_tests import suite as switch_center_suite
from openheating.tests.config_parser_tests import suite as config_parser_suite

from openheating.dbus.tests.easy_suite import suite as dbus_suite
from openheating.hardware.tests.easy_suite import suite as hardware_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(sink_suite)
suite.addTest(transport_suite)
suite.addTest(oil_combo_suite)
#suite.addTest(burner_suite)
suite.addTest(thermometer_center_suite)
suite.addTest(switch_center_suite)
suite.addTest(config_parser_suite)

suite.addTest(dbus_suite)
suite.addTest(hardware_suite)
