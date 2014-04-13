from heating.tests.transport_tests import suite as transport_suite
from heating.tests.burner_tests import suite as burner_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(transport_suite)
suite.addTest(burner_suite)
