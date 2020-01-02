from openheating.base.error import HeatingError
from openheating.dbus.error import DBusHeatingError

import unittest
import json


class DBusErrorTest(unittest.TestCase):

    def test__transport_HeatingError(self):
        server_error = HeatingError('dis is da message')
        self.assertEqual(server_error.details['category'], 'general')
        self.assertEqual(server_error.details['message'], 'dis is da message')

        transport_error = DBusHeatingError(server_error.details)

        # server side: pydbus calls str() on the exception, which we
        # define as a json dictionary.
        str_json = transport_error.to_json()
        str_str = str(transport_error)
        self.assertEqual(str_str, str_json)

        # json string travels across dbus
        client_error = DBusHeatingError.from_json(str_json)
        self.assertEqual(client_error.details['category'], 'general')
        self.assertEqual(client_error.details['message'], 'dis is da message')

suite = unittest.defaultTestLoader.loadTestsFromTestCase(DBusErrorTest)

if __name__ == '__main__':
    unittest.main()
