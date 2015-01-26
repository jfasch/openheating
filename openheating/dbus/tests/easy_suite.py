from openheating.dbus.tests.basic_tests import suite as basic_suite
from openheating.dbus.tests.client_tests import suite as client_suite
from openheating.dbus.tests.object_tests import suite as object_suite
from openheating.dbus.tests.service_tests import suite as service_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(basic_suite)
suite.addTest(client_suite)
suite.addTest(object_suite)
suite.addTest(service_suite)
