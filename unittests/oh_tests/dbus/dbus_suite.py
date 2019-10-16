from .exception_suite import suite as exception_suite
from .thermometer_service_suite import suite as thermometer_service_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(exception_suite)
suite.addTest(thermometer_service_suite)

