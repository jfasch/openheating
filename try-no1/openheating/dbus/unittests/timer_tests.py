from openheating.dbus.unittests.dbus_testcase import DBusTestCase

from openheating.dbus.object import DBusObject, DBusObjectCreator
from openheating.dbus.service import DBusService
from openheating.dbus.client import DBusObjectClient
from openheating.dbus.connection import DBusClientConnection

import dbus
from gi.repository import GObject

import unittest
import time


class TimerTest(DBusTestCase):
    def test__basic(self):
        INTERVAL = 0.1

        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/timer': _ObjectWithTimerCreator(interval=INTERVAL)})
        self.add_and_start_service(service)
        self.wait_for_object('some.dbus.service', '/timer')

        client = DBusObjectClient(connection=DBusClientConnection(address=self.daemon_address()),
                                  name='some.dbus.service', path='/timer')

        # wait untils the object's timer has expired at least three
        # times
        num_loops = 0
        while client.client_call('num_expires') < 3:
            time.sleep(INTERVAL)
            self.assertTrue(num_loops < 100)
            num_loops += 1


class _ObjectWithTimerCreator(DBusObjectCreator):
    def __init__(self, interval):
        DBusObjectCreator.__init__(self)
        self.__interval = interval

    def create_object(self, path):
        class ObjectWithTimer(DBusObject):
            def __init__(self, path, interval):
                DBusObject.__init__(self, path)
                self.__num_expires = 0
                self.__timer = GObject.timeout_add_seconds(interval, self.__expired)

            @dbus.service.method(dbus_interface='my.dumb.thing', out_signature='i')
            def num_expires(self):
                return self.__num_expires

            def __expired(self):
                self.__num_expires += 1
                return True # call me again
                
        return ObjectWithTimer(path, self.__interval)
        



        
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TimerTest)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
