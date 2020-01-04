from .dbussuite_exception import suite as exception_suite
from .dbussuite_lifecycle import suite as lifecycle_suite
from .dbussuite_thermometers import suite as thermometers_suite
from .dbussuite_switches import suite as switches_suite
from .dbussuite_circuits import suite as circuits_suite
from .dbussuite_main import suite as main_suite
from .dbussuite_errors import suite as errors_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(exception_suite)
suite.addTest(lifecycle_suite)
suite.addTest(thermometers_suite)
suite.addTest(switches_suite)
suite.addTest(circuits_suite)
suite.addTest(main_suite)
suite.addTest(errors_suite)

