from openheating.error import HeatingError

from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.exception_tester import ExceptionTester_Client

import pydbus

import unittest
import subprocess
import json


class ExceptionTest(unittest.TestCase):
    def setUp(self):
        self.__service = services.ExceptionTesterService()

    def tearDown(self):
        self.__service.stop()
        
    def test__HeatingError(self):
        client = ExceptionTester_Client(pydbus.SessionBus())
        self.assertRaises(HeatingError, client.raise_default_HeatingError, 'message')

    def test__HeatingError_default_json_payload(self):
        client = ExceptionTester_Client(pydbus.SessionBus())
        try:
            client.raise_default_HeatingError('the message')
        except HeatingError as e:
            self.assertEqual(e.details['type'], 'HeatingError')
            self.assertEqual(e.details['message'], 'the message')

    def test__derived_default_HeatingError(self):
        client = ExceptionTester_Client(pydbus.SessionBus())
        try:
            client.raise_derived_default_HeatingError('the message')
        except HeatingError as e:
            self.assertEqual(e.details['type'], 'HeatingError')
            self.assertEqual(e.details['message'], 'the message')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExceptionTest))

if __name__ == '__main__':
    testutils.run(suite)
