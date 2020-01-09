from openheating.dbus import dbusutil
from openheating.dbus import lifecycle
from openheating.test import testutils
from openheating.test import service
from openheating.test.plant_testcase import PlantTestCase
from openheating.test.plant import Plant

from gi.repository import GLib

import unittest
import time
import signal
import os.path


class ManagedTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__directory = self.tempdir()
        
    def test__basic(self):
        self.start_plant(Plant([service.ManagedObjectTesterService(stampdir=self.__directory.name)]))
        self.stop_plant()
        self.assertTrue(os.path.isfile(self.__directory.name+'/started'))
        self.assertTrue(os.path.isfile(self.__directory.name+'/stopped'))


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ManagedTest))

if __name__ == '__main__':
    testutils.run(suite)
