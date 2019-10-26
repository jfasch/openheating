from openheating.error import HeatingError

from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.exception_tester import ExceptionTester_Client

import pydbus

import unittest
import subprocess
import json


class ExceptionTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.start_services([services.ExceptionTesterService()])
        
    def test__HeatingError(self):
        client = ExceptionTester_Client(pydbus.SessionBus())
        self.assertRaises(HeatingError, client.raise_default_HeatingError, 'message')

    def test__HeatingError_default_json_payload(self):
        client = ExceptionTester_Client(pydbus.SessionBus())
        try:
            client.raise_default_HeatingError('the message')
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'general')
        self.assertEqual(exc.details['message'], 'the message')

    def test__derived_default_HeatingError(self):
        client = ExceptionTester_Client(pydbus.SessionBus())
        try:
            client.raise_derived_default_HeatingError('the message')
            self.fail()
        except HeatingError as e:
            exc = e
        self.assertEqual(exc.details['category'], 'general')
        self.assertEqual(exc.details['message'], 'the message')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExceptionTest))

if __name__ == '__main__':
    testutils.run(suite)
