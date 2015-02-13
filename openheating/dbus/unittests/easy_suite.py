from .basic_tests import suite as basic_suite
from .client_tests import suite as client_suite
from .object_tests import suite as object_suite
from .service_tests import suite as service_suite
from .error_tests import suite as error_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(basic_suite)
suite.addTest(client_suite)
suite.addTest(object_suite)
suite.addTest(service_suite)
suite.addTest(error_suite)
