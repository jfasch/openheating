from .easysuite_nodedef import suite as nodedef_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(nodedef_suite)

