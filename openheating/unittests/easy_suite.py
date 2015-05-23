from openheating.base.unittests.easy_suite import suite as base_suite
from openheating.logic.unittests.easy_suite import suite as logic_suite
from openheating.testutils.unittests.easy_suite import suite as testutils_suite
from openheating.dbus.unittests.easy_suite import suite as dbus_suite
from openheating.hardware.unittests.easy_suite import suite as hardware_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(base_suite)
suite.addTest(logic_suite)
suite.addTest(testutils_suite)
suite.addTest(dbus_suite)
suite.addTest(hardware_suite)
