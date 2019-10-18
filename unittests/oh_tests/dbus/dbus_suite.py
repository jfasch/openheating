from .graceful_termination_suite import suite as graceful_termination_suite
from .exception_suite import suite as exception_suite
from .lifecycle_suite import suite as lifecycle_suite
from .thermometer_service_suite import suite as thermometer_service_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(graceful_termination_suite)
suite.addTest(exception_suite)
suite.addTest(lifecycle_suite)
suite.addTest(thermometer_service_suite)

