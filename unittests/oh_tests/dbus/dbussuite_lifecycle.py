from openheating.dbus import dbusutil
from openheating.dbus import lifecycle
from openheating.test import testutils
from openheating.test import services

from gi.repository import GLib

import unittest
import tempfile
import time
import signal
import os.path


class ManagedTest(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.__directory = tempfile.TemporaryDirectory()
    def tearDown(self):
        self.__directory.cleanup()
        
    def test__basic(self):
        self.start_services([services.ManagedObjectTesterService(stampdir=self.__directory.name)])
        self.stop_services()
        self.assertTrue(os.path.isfile(self.__directory.name+'/started'))
        self.assertTrue(os.path.isfile(self.__directory.name+'/stopped'))


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ManagedTest))

if __name__ == '__main__':
    testutils.run(suite)
