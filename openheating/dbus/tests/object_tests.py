from openheating.dbus.object import DBusObject
from openheating.dbus.rebind import DBusObjectClient
from openheating.dbus.rebind import DBusClientConnection
from openheating.dbus.rebind import DBusServerConnection

from openheating.testutils.dbus_testcase import DBusTestCase

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

import unittest
import os
import sys
import signal
import time

class ObjectTest(DBusTestCase):
    def setUp(self):
        self.__pid = None
        super().setUp()

    def tearDown(self):
        if self.__pid is not None:
            os.kill(self.__pid, signal.SIGKILL)
            os.waitpid(self.__pid, 0)
        super().tearDown()

    def test__basic(self):
        self.__pid = os.fork()

        if self.__pid == 0: # child

            # funny things happening; still don't know for sure what's
            # going on.

            # os.setpgid(0,0) # jjjj ????
            # signal.signal(signal.SIGTERM, signal.SIG_IGN) # jjjj

            mainloop = DBusGMainLoop(set_as_default=True)
            connection = dbus.bus.BusConnection(self.daemon_address(), mainloop=mainloop)
            busname = dbus.service.BusName(name='some.bus.name', bus=connection)
            server_conn = DBusServerConnection(connection)
            echo_object = EchoObject(server_conn.get_connection(), '/path/to/echo')
            GLib.MainLoop().run()
            sys.exit()
        else: # parent
            self.wait_for_object('some.bus.name', '/path/to/echo')
            client = DBusObjectClient(
                connection=DBusClientConnection(address=self.daemon_address()), 
                name='some.bus.name',
                path='/path/to/echo')
            result = client.dbus_call('echo', 'hallo')
            self.assertEqual(result, 'hallo')
            

class EchoObject(DBusObject):
    @dbus.service.method(dbus_interface='some.lousy.echo', in_signature = 's', out_signature = 's')
    def echo(self, string):
        return string
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ObjectTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
