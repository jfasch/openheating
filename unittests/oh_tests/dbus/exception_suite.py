from openheating.error import HeatingError

from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.exception_tester import ExceptionTester_Client

import pydbus

import unittest
import subprocess


class ExceptionTest(unittest.TestCase):
    def setUp(self):
        self.__service = services.ExceptionTesterService()

    def tearDown(self):
        self.__service.stop()
        
    def test__HeatingError_python_client(self):
        client = ExceptionTester_Client(pydbus.SessionBus())
        self.assertRaises(HeatingError, client.raise_base_HeatingError, 'message')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExceptionTest))

if __name__ == '__main__':
    testutils.run(suite)
