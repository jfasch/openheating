from openheating.testutils.dbus_testcase import DBusTestCase

import dbus.bus

import unittest


class BasicTest(DBusTestCase):
    def test__daemon_running(self):
        bus_connection = dbus.bus.BusConnection(self.daemon_address())
        bus_object = bus_connection.get_object('org.freedesktop.DBus', '/')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BasicTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
