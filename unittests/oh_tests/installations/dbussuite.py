from .dbussuite_faschingbauer import suite as faschingbauer_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(faschingbauer_suite)
