from openheating.dbus.tests.thermometer_service_tests import suite as thermometer_service_suite
from openheating.dbus.tests.thermometer_center_tests import suite as thermometer_center_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(thermometer_service_suite)
suite.addTest(thermometer_center_suite)
