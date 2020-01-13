from openheating.base.error import HeatingError

from openheating.testutils import testutils
from openheating.testutils.plant_testcase import PlantTestCase
from openheating.plant import service
from openheating.plant.plant import Plant

from openheating.dbus import dbusutil
from openheating.dbus.exception_tester import ExceptionTester_Client
from openheating.dbus.errors import Errors_Client

import unittest
import subprocess
import json


class ExceptionTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.start_plant(Plant([service.ExceptionTesterService(),
                                service.ErrorService()]))

    @PlantTestCase.intercept_failure
    def test__HeatingError(self):
        exctester_client = ExceptionTester_Client(self.bus)
        try:
            exctester_client.raise_default_HeatingError('the message')
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'general')
        self.assertEqual(exc.details['message'], 'the message')

        # a HeatingError is not implicitly signaled onto the bus, so
        # the errors services cannot pick it up.
        errors_client = Errors_Client(self.bus)
        self.assertEqual(errors_client.num_errors(), 0)

    @PlantTestCase.intercept_failure
    def test__derived_default_HeatingError(self):
        exctester_client = ExceptionTester_Client(self.bus)
        try:
            exctester_client.raise_derived_default_HeatingError('the message')
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'general')
        self.assertEqual(exc.details['message'], 'the message')

        # a HeatingError is not implicitly signaled onto the bus, so
        # the errors services cannot pick it up.
        errors_client = Errors_Client(self.bus)
        self.assertEqual(errors_client.num_errors(), 0)

    @PlantTestCase.intercept_failure
    def test__non_HeatingError(self):
        exctester_client = ExceptionTester_Client(self.bus)
        try:
            exctester_client.raise_non_HeatingError()
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'general')
        self.assertIn('message', exc.details)
        # fixme: check for traceback

        # non-HeatingErrors are signaled on the bus, so the errors
        # service picks it up.
        errors_client = Errors_Client(self.bus)
        self.assertEqual(errors_client.num_errors(), 1)

        error = errors_client.get_errors()[0]
        self.assertEqual(error.details['category'], 'general')
        self.assertIn('message', error.details)
        # fixme: check for traceback
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExceptionTest))

if __name__ == '__main__':
    testutils.run(suite)
