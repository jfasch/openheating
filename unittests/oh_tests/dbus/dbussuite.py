from .dbussuite_exception import suite as exception_suite
from .dbussuite_lifecycle import suite as lifecycle_suite
from .dbussuite_thermometers import suite as thermometers_suite
from .dbussuite_errors import suite as errors_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(exception_suite)
suite.addTest(lifecycle_suite)
suite.addTest(thermometers_suite)
suite.addTest(errors_suite)

