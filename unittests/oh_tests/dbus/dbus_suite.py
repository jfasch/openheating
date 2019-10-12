from .thermometer_service_suite import suite as thermometer_service_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(thermometer_service_suite)

