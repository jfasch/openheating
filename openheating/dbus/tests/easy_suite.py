from openheating.dbus.tests.service_tests import suite as service_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(service_suite)
