from openheating.dbus.service import Creator, DBusService
from openheating.dbus.object import DBusObject
from openheating.dbus.rebind import DBusObjectClient, DBusClientConnection
import openheating.dbus.types as types
from openheating.testutils.dbus_testcase import DBusTestCase
from openheating.error import HeatingError

import dbus
import unittest


class ErrorTest(DBusTestCase):
    def setUp(self):
        self.__services = []
        super().setUp()

    def tearDown(self):
        for s in self.__services:
            s.stop()
        super().tearDown()

    def test__conversion__single_error__no_dbus__in_process(self):
        orig_err = HeatingError(msg='the-message')
        dbus_err = types.exception_local_to_dbus(orig_err)
        err = types.exception_dbus_to_local(dbus_err)
        self.assertIsInstance(err, HeatingError)
        self.assertEqual(err.args[0], orig_err.args[0])
        self.assertEqual(err.msg(), orig_err.msg())

    def test__single_heating_error__idempotent(self):
        class SingleErrorObjectCreator(Creator):
            def create_dbus_object(self, connection, path):
                class SingleErrorObject(DBusObject):
                    @dbus.service.method(dbus_interface='my.dumb.Raiser')
                    def raise_the_thing(self):
                        raise types.exception_local_to_dbus(HeatingError('the-message'))
                return SingleErrorObject(connection, path)
            def create_native_object(self): 
                assert False

        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/error': SingleErrorObjectCreator()})
        self.__services.append(service)
        service.start()
        self.wait_for_object('some.dbus.service', '/error')

        try:
            client = DBusObjectClient(connection=DBusClientConnection(address=self.daemon_address()),
                             name='some.dbus.service', path='/error')
            client.dbus_call('raise_the_thing')
        except HeatingError as e:
            my_exc = e

        self.assertEqual(my_exc.args[0], 'the-message')

    def test__server_side_interpreter_errors_assert_at_client(self):
        '''Remote side encounters a "program error" - some assertion, or a
        python interpreter error (e.g. a NameError). This must not get
        through unrecognized, but rather raise an assertion at the
        client.'''

        class NameErrorObjectCreator(Creator):
            def create_dbus_object(self, connection, path):
                class NameErrorObject(DBusObject):
                    @dbus.service.method(dbus_interface='my.dumb.Error')
                    def do_the_error(self):
                        # this raises a NameError (anything but a
                        # HeatingError will do)
                        x = some_unknown_name
                return NameErrorObject(connection, path)
            def create_native_object(self): 
                assert False

        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/error': NameErrorObjectCreator()})
        self.__services.append(service)
        service.start()
        self.wait_for_object('some.dbus.service', '/error')

        client = DBusObjectClient(connection=DBusClientConnection(address=self.daemon_address()),
                                  name='some.dbus.service', path='/error')
        self.assertRaises(AssertionError, client.dbus_call, 'do_the_error')

        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ErrorTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
