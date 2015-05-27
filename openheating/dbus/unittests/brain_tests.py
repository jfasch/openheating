from openheating.dbus.unittests.dbus_testcase import DBusTestCase

from openheating.dbus.client_brain import DBusBrainClient
from openheating.dbus.connection import DBusClientConnection
from openheating.dbus.service import DBusService
from openheating.dbus.service_config_object import BrainObjectCreator
from openheating.logic.thinker import LeafThinker

import unittest


class BrainTest(DBusTestCase):
    def test__nothing_to_think(self):
        class MyThinker(LeafThinker):
            def think(self):
                return []

            
        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/brain': BrainObjectCreator([MyThinker('thinker')])})
        self.add_and_start_service(service)
        self.wait_for_object('some.dbus.service', '/error')

        client = DBusBrainClient(connection=DBusClientConnection(address=self.daemon_address()),
                                 name='some.dbus.service', path='/brain')

        result = client.think()
        self.assertEqual(len(result), 0)
        
    def test__think_loop(self):
        class MyThinker(LeafThinker):
            def __init__(self, name):
                LeafThinker.__init__(self, name)
                self.__num_loop = 0
            def think(self):
                if self.__num_loop == 2:
                    ret = []
                else:
                    ret = [(self.name(), 'message')]
                self.__num_loop += 1
                return ret
            
        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/brain': BrainObjectCreator([MyThinker('thinker')])})
        self.add_and_start_service(service)
        self.wait_for_object('some.dbus.service', '/error')

        client = DBusBrainClient(connection=DBusClientConnection(address=self.daemon_address()),
                                 name='some.dbus.service', path='/brain')

        result = client.think()

        self.assertEqual(len(result), 2)
        self.assertEqual(result, [(0, [('thinker', 'message')]), (1, [('thinker', 'message')])])
        
        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BrainTest))
#suite.addTest(ErrorTest('test__nested_errors'))
#suite.addTest(ErrorTest('test__dbus_conversion'))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
