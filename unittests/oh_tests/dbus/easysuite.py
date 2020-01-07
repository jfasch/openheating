from .easysuite_error import suite as error_suite
from .easysuite_nodedef import suite as nodedef_suite
from .easysuite_switches_pyconf import suite as switches_pyconf_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(error_suite)
suite.addTest(nodedef_suite)
suite.addTest(switches_pyconf_suite)

