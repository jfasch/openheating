from .dbus_testcase import DBusTestCase

import dbus.bus
import unittest


class BasicTest(DBusTestCase):
    def test__daemon_running(self):
        bus_connection = dbus.bus.BusConnection(self.daemon_address())
        bus_object = bus_connection.get_object('org.freedesktop.DBus', '/')
        bus_object.GetId()

    def test__restart_daemon(self):
        bus_connection = dbus.bus.BusConnection(self.daemon_address())
        bus_object = bus_connection.get_object('org.freedesktop.DBus', '/')
        bus_object.GetId()

        self.stop_daemon()

        self.assertRaises(dbus.exceptions.DBusException, bus_object.GetId)
            
        self.start_daemon()

        bus_connection = dbus.bus.BusConnection(self.daemon_address())
        bus_object = bus_connection.get_object('org.freedesktop.DBus', '/')
        bus_object.GetId()

        self.restart_daemon()

        self.assertRaises(dbus.exceptions.DBusException, bus_object.GetId)

        bus_connection = dbus.bus.BusConnection(self.daemon_address())
        bus_object = bus_connection.get_object('org.freedesktop.DBus', '/')
        bus_object.GetId()

        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BasicTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
