from .dbussuite_exception import suite as exception_suite
from .dbussuite_lifecycle import suite as lifecycle_suite
from .dbussuite_thermometer_service import suite as thermometer_service_suite
from .dbussuite_error_service import suite as error_service_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(exception_suite)
suite.addTest(lifecycle_suite)
suite.addTest(thermometer_service_suite)
suite.addTest(error_service_suite)

