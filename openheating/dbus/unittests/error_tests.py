from .dbus_testcase import DBusTestCase

from openheating.dbus.service import DBusObjectCreator, DBusService
from openheating.dbus.object import DBusObject
from openheating.dbus.client import DBusObjectClient
from openheating.dbus.connection import DBusClientConnection
import openheating.dbus.types as types
from openheating.base.error import HeatingError

import dbus
import unittest


class ErrorTest(DBusTestCase):
    def test__error_equality(self):
        self.assertTrue(HeatingError.equal(
            HeatingError(msg='xxx', permanent=False),
            HeatingError(msg='xxx', permanent=False)))
        self.assertFalse(HeatingError.equal(
            HeatingError(msg='xxx', permanent=False),
            HeatingError(msg='yyy', permanent=False)))
        self.assertFalse(HeatingError.equal(
            HeatingError(msg='xxx', permanent=False),
            HeatingError(msg='xxx', permanent=True)))

        # nested ...
        self.assertTrue(HeatingError.equal(
            HeatingError(msg='xxx', permanent=False, nested_errors=[HeatingError(msg='yyy', permanent=False)]),
            HeatingError(msg='xxx', permanent=False, nested_errors=[HeatingError(msg='yyy', permanent=False)])))
        self.assertFalse(HeatingError.equal(
            HeatingError(msg='xxx', permanent=False, nested_errors=[HeatingError(msg='yyy', permanent=False)]),
            HeatingError(msg='xxx', permanent=False, nested_errors=[HeatingError(msg='yyy', permanent=True)])))

    def test__dbus_conversion(self):
        orig_err = HeatingError(msg='xxx', permanent=False)
        err = types.exception_dbus_to_local(types.exception_local_to_dbus(orig_err))
        self.assertIsInstance(err, HeatingError)
        self.assertTrue(HeatingError.equal(orig_err, err))

        # a permanent one, this time
        orig_err = HeatingError(msg='xxx', permanent=True)
        err = types.exception_dbus_to_local(types.exception_local_to_dbus(orig_err))
        self.assertIsInstance(err, HeatingError)
        self.assertTrue(HeatingError.equal(orig_err, err))

        # nested
        if True:
            orig_err = HeatingError(msg='xxx', permanent=False, nested_errors=[HeatingError(msg='yyy', permanent=True)])
            err = types.exception_dbus_to_local(types.exception_local_to_dbus(orig_err))
            self.assertIsInstance(err, HeatingError)
            self.assertTrue(HeatingError.equal(orig_err, err))

            orig_err = HeatingError(msg='xxx', permanent=False, nested_errors=[HeatingError(msg='yyy', permanent=True),
                                                                               HeatingError(msg='zzz', permanent=False)])
            err = types.exception_dbus_to_local(types.exception_local_to_dbus(orig_err))
            self.assertIsInstance(err, HeatingError)
            self.assertTrue(HeatingError.equal(orig_err, err))

            orig_err = HeatingError(msg='xxx', permanent=True,
                                    nested_errors=[
                                        HeatingError(msg='yyy1', permanent=False,
                                                     nested_errors=[HeatingError(msg='zzz1', permanent=True)]),
                                        HeatingError(msg='yyy2', permanent=False,
                                                     nested_errors=[HeatingError(msg='zzz2', permanent=False)])])
            err = types.exception_dbus_to_local(types.exception_local_to_dbus(orig_err))
            self.assertIsInstance(err, HeatingError)
            self.assertTrue(HeatingError.equal(orig_err, err))
            
    def test__single_heating_error__idempotent(self):
        class SingleErrorObjectCreator(DBusObjectCreator):
            def create_object(self, path):
                class SingleErrorObject(DBusObject):
                    @dbus.service.method(dbus_interface='my.dumb.Raiser')
                    def raise_the_thing(self):
                        raise types.exception_local_to_dbus(HeatingError(permanent=False, msg='the-message'))
                return SingleErrorObject(path)

        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/error': SingleErrorObjectCreator()})
        self.add_and_start_service(service)
        self.wait_for_object('some.dbus.service', '/error')

        try:
            client = DBusObjectClient(connection=DBusClientConnection(address=self.daemon_address()),
                             name='some.dbus.service', path='/error')
            client.client_call('raise_the_thing')
        except HeatingError as e:
            my_exc = e

        self.assertEqual(my_exc.args[0], 'the-message')

    def test__server_side_interpreter_errors_assert_at_client(self):
        # Remote side encounters a "program error" - some assertion,
        # or a python interpreter error (e.g. a NameError). This must
        # not get through unrecognized, but rather raise an assertion
        # at the client.

        class NameErrorObjectCreator(DBusObjectCreator):
            def create_object(self, path):
                class NameErrorObject(DBusObject):
                    @dbus.service.method(dbus_interface='my.dumb.Error')
                    def do_the_error(self):
                        # this raises a NameError (anything but a
                        # HeatingError will do)
                        x = some_unknown_name
                return NameErrorObject(path)

        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/error': NameErrorObjectCreator()})
        self.add_and_start_service(service)
        self.wait_for_object('some.dbus.service', '/error')

        client = DBusObjectClient(connection=DBusClientConnection(address=self.daemon_address()),
                                  name='some.dbus.service', path='/error')
        self.assertRaises(AssertionError, client.client_call, 'do_the_error')


    remote_nested_error = HeatingError(msg='xxx', permanent=True,
                                       nested_errors=[
                                           HeatingError(msg='yyy1', permanent=False,
                                                        nested_errors=[HeatingError(msg='zzz1', permanent=True)]),
                                           HeatingError(msg='yyy2', permanent=False,
                                                        nested_errors=[HeatingError(msg='zzz2', permanent=False)])])

    def test__nested_errors(self):
        class NestedRaiserObjectCreator(DBusObjectCreator):
            def create_object(self, path):
                class NestedRaiserObject(DBusObject):
                    @dbus.service.method(dbus_interface='my.dumb.Raiser.do_nested_error')
                    def do_nested_error(self):
                        raise types.exception_local_to_dbus(ErrorTest.remote_nested_error)
                return NestedRaiserObject(path)

        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={'/raiser': NestedRaiserObjectCreator()})
        self.add_and_start_service(service)
        self.wait_for_object('some.dbus.service', '/raiser')

        client = DBusObjectClient(connection=DBusClientConnection(address=self.daemon_address()),
                                  name='some.dbus.service', path='/raiser')
        try:
            client.client_call('do_nested_error')
            self.fail()
        except HeatingError as e:
            local_error = e

        self.assertTrue(HeatingError.equal(local_error, self.remote_nested_error))
        
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ErrorTest))
#suite.addTest(ErrorTest('test__nested_errors'))
#suite.addTest(ErrorTest('test__dbus_conversion'))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
