from .sink_tests import suite as sink_suite
from .transport_tests import suite as transport_suite
#from .burner_tests import suite as burner_suite
from .thermometer_manager_tests import suite as thermometer_manager_suite
from .thermometer_dbus_service_tests import suite as thermometer_dbus_service_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(sink_suite)
suite.addTest(transport_suite)
#suite.addTest(burner_suite)
suite.addTest(thermometer_manager_suite)
suite.addTest(thermometer_dbus_service_suite)
