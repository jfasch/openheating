from openheating.base.error import HeatingError

from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.exception_tester import ExceptionTester_Client
from openheating.dbus.errors import Errors_Client

import pydbus

import unittest
import subprocess
import json


class ExceptionTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.start_services([services.ExceptionTesterService(),
                             services.ErrorService()])

    @services.ServiceTestCase.intercept_failure
    def test__HeatingError(self):
        exctester_client = ExceptionTester_Client(pydbus.SessionBus())
        try:
            exctester_client.raise_default_HeatingError('the message')
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'general')
        self.assertEqual(exc.details['message'], 'the message')

        # a HeatingError is not implicitly signaled onto the bus, so
        # the errors services cannot pick it up.
        errors_client = Errors_Client(pydbus.SessionBus())
        self.assertEqual(errors_client.num_errors(), 0)

    @services.ServiceTestCase.intercept_failure
    def test__derived_default_HeatingError(self):
        exctester_client = ExceptionTester_Client(pydbus.SessionBus())
        try:
            exctester_client.raise_derived_default_HeatingError('the message')
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'general')
        self.assertEqual(exc.details['message'], 'the message')

        # a HeatingError is not implicitly signaled onto the bus, so
        # the errors services cannot pick it up.
        errors_client = Errors_Client(pydbus.SessionBus())
        self.assertEqual(errors_client.num_errors(), 0)

    @services.ServiceTestCase.intercept_failure
    def test__non_HeatingError(self):
        exctester_client = ExceptionTester_Client(pydbus.SessionBus())
        try:
            exctester_client.raise_non_HeatingError()
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'internal')
        self.assertIn('message', exc.details)
        self.assertIn('traceback', exc.details)

        # non-HeatingErrors are signaled on the bus, so the errors
        # service picks it up.
        errors_client = Errors_Client(pydbus.SessionBus())
        self.assertEqual(errors_client.num_errors(), 1)

        error = errors_client.get_errors()[0]
        self.assertEqual(error.details['category'], 'internal')
        self.assertIn('message', error.details)
        self.assertIn('traceback', error.details)
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExceptionTest))

if __name__ == '__main__':
    testutils.run(suite)
