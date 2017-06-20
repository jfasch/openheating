from .thermometer_test import suite as thermometer_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(thermometer_suite)
