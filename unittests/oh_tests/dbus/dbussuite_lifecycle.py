from openheating.dbus import lifecycle
from openheating.testutils import testutils
from openheating.testutils.plant_testcase import PlantTestCase
from openheating.plant.service_def import ManagedObjectTesterService
from openheating.plant.plant import Plant

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
        self.start_plant(Plant([
            ManagedObjectTesterService(stampdir=self.__directory.name),
        ]))
        self.stop_plant()
        self.assertTrue(os.path.isfile(self.__directory.name+'/started'))
        self.assertTrue(os.path.isfile(self.__directory.name+'/stopped'))


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ManagedTest))

if __name__ == '__main__':
    testutils.run(suite)
