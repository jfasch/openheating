from openheating.dbus.unittests.dbus_testcase import DBusTestCase

from openheating.dbus.object_looper import LooperObjectCreator
from openheating.dbus.client_looper import DBusLooperClient
from openheating.dbus.object_brain import BrainObjectCreator
from openheating.dbus.client_brain import DBusBrainClient
from openheating.dbus.connection import DBusClientConnection
from openheating.dbus.service import DBusService
from openheating.dbus.service_config_native import NativeObject
from openheating.logic.thinker import LeafThinker

import unittest
import time


class LooperTest(DBusTestCase):
    def test__basic(self):
        class MyThinker(LeafThinker):
            def think(self):
                return []

            
        brain_service = DBusService(
            daemon_address=self.daemon_address(),
            name='brain.service',
            object_creators={'/brain': BrainObjectCreator([MyThinker('thinker')])})
        self.add_and_start_service(brain_service)
        self.wait_for_object('brain.service', '/brain')

        looper_service = DBusService(
            daemon_address=self.daemon_address(),
            name='looper.service',
            object_creators={'/looper': LooperObjectCreator(interval_seconds=0.1, brain=NativeObject(DBusBrainClient, name='brain.service', path='/brain'), triggers=[])})
        self.add_and_start_service(looper_service)
        self.wait_for_object('looper.service', '/looper')

        looper_client = DBusLooperClient(connection=DBusClientConnection(address=self.daemon_address()),
                                  name='looper.service', path='/looper')

        num_loops = 0
        while looper_client.num_loops() < 10:
            time.sleep(0.2)
            num_loops += 1
            self.assertTrue(num_loops < 100)
        
        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LooperTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
