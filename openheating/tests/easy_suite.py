from .sink_tests import suite as sink_suite
from .transport_tests import suite as transport_suite
#from .burner_tests import suite as burner_suite
from .thermometer_center_tests import suite as thermometer_center_suite
from .thermometer_dbus_service_tests import suite as thermometer_dbus_service_suite
from .config_tests import suite as config_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(sink_suite)
suite.addTest(transport_suite)
#suite.addTest(burner_suite)
suite.addTest(thermometer_center_suite)
suite.addTest(thermometer_dbus_service_suite)
suite.addTest(config_suite)
