from .gpio_tests import suite as gpio_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(gpio_suite)
