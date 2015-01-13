from openheating.error import DBusNoConnectionError
from openheating.dbus.rebind import DBusClientConnection
from openheating.dbus.rebind import DBusObjectClient
from openheating.testutils.dbus_testcase import DBusTestCase

import dbus.bus
import unittest


class ClientTest(DBusTestCase):
    def test__establish_connection(self):
        connection = DBusClientConnection(address=self.daemon_address())
        bus_object = connection.get_connection().get_object('org.freedesktop.DBus', '/')
        bus_object.GetId()

    def test__reestablish_connection(self):
        connection = DBusClientConnection(address=self.daemon_address())
        bus_object = connection.get_connection().get_object('org.freedesktop.DBus', '/')
        bus_object.GetId()

        self.restart_daemon()
        
        self.assertRaises(dbus.exceptions.DBusException, bus_object.GetId)

        connection.clear_connection()
        bus_object = connection.get_connection().get_object('org.freedesktop.DBus', '/')

    def test__object_client__connection_loss(self):
        client = DBusObjectClient(
            connection=DBusClientConnection(address=self.daemon_address()),
            name='org.freedesktop.DBus',
            path='/')
        client.dbus_call('GetId')

        self.restart_daemon()

        # raises DBusNoConnectionError at first call after connection
        # loss
        self.assertRaises(DBusNoConnectionError, client.dbus_call, 'GetId')

        # re-establishes connection at second
        client.dbus_call('GetId')


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ClientTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
