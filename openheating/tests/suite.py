from .sink_tests import suite as sink_suite
from .transport_tests import suite as transport_suite
#from .burner_tests import suite as burner_suite
from .thermometer_tests import suite as thermometer_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(sink_suite)
suite.addTest(transport_suite)
#suite.addTest(burner_suite)
suite.addTest(thermometer_suite)
