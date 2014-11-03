from openheating.tests.transport_tests import suite as transport_suite
from openheating.tests.producer_overheat_tests import suite as producer_overheat_suite
from openheating.tests.burner_tests import suite as burner_suite
from openheating.tests.thermometer_tests import suite as thermometer_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(transport_suite)
suite.addTest(producer_overheat_suite)
suite.addTest(burner_suite)
suite.addTest(thermometer_suite)
