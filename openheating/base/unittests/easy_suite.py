from .config_parser_tests import suite as config_parser_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(config_parser_suite)
