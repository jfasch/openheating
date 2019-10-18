from openheating.dbus import dbusutil
from openheating.test import testutils
from openheating.test import services

import pydbus

import unittest
import tempfile
import time
import os.path


class LifecycleTest(unittest.TestCase):
    def setUp(self):
        self.__directory = tempfile.TemporaryDirectory()
        self.__service = services.LifecycleTesterService(stampdir=self.__directory.name)
    def tearDown(self):
        self.__directory.cleanup()
        
    def test__basic(self):
        self.__service.start(suppress_stderr=False)
        self.__service.stop()
        self.assertTrue(os.path.isfile(self.__directory.name+'/started'))
        self.assertTrue(os.path.isfile(self.__directory.name+'/stopped'))


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LifecycleTest))

if __name__ == '__main__':
    testutils.run(suite)
