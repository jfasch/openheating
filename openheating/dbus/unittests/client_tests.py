from .dbus_testcase import DBusTestCase

from openheating.base.error import HeatingError
from openheating.dbus.connection import DBusClientConnection
from openheating.dbus.client import DBusObjectClient

import dbus.bus
import unittest


class ClientTest(DBusTestCase):
    def test__establish_connection(self):
        connection = DBusClientConnection(address=self.daemon_address())
        proxy = connection.get_proxy('org.freedesktop.DBus', '/')
        proxy.GetId()

    def test__reestablish_connection(self):
        connection = DBusClientConnection(address=self.daemon_address())
        proxy = connection.get_proxy('org.freedesktop.DBus', '/')
        proxy.GetId()

        self.restart_daemon()
        
        self.assertRaises(dbus.exceptions.DBusException, proxy.GetId)

        connection.connection_lost()
        proxy = connection.get_proxy('org.freedesktop.DBus', '/')

    def test__object_client__connection_loss(self):
        client = DBusObjectClient(
            connection=DBusClientConnection(address=self.daemon_address()),
            name='org.freedesktop.DBus',
            path='/')
        client.client_call('GetId')

        self.restart_daemon()

        self.assertRaises(HeatingError, client.client_call, 'GetId')

        # re-establishes connection at second
        client.client_call('GetId')


suite = unittest.defaultTestLoader.loadTestsFromTestCase(ClientTest)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
