from .easysuite_error import suite as error_suite
from .easysuite_nodedef import suite as nodedef_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(error_suite)
suite.addTest(nodedef_suite)

