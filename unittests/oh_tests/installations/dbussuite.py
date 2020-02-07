from .dbussuite_faschingbauer import suite as faschingbauer_suite
from .dbussuite_systemd_generator import suite as systemd_generator_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(faschingbauer_suite)
suite.addTest(systemd_generator_suite)
