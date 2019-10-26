from openheating.error import HeatingError
from openheating.dbus.thermometer_center import ThermometerCenter_Client

from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.errors import Errors_Client

import pydbus

import unittest
import subprocess
import time
import sys


class ErrorServiceTest(services.ServiceTestCase):

    @services.ServiceTestCase.intercept_failure
    def test__basic_error_count(self):
        self.add_service(services.ErrorService())
        self.add_service(services.ThermometerService(
            pyconf=[
                "from openheating.thermometer import ErrorThermometer",
                "THERMOMETERS['Error'] = ErrorThermometer(",
                "    name='Error',",
                "    description='Error Thermometer',",
                "    n_ok_before_error=0)"
            ]))

        self.start_services()
        self.__wait_error_occurred()

    # def test__w1__file_not_found(self):
    #     self.fail('jjjj')
    #     try:
    #         error_service = services.ErrorService()
    #         thermometer_service = services.ThermometerService(
    #             pyconf=[
    #                 "from openheating.w1 import W1Thermometer",
    #                 "THERMOMETERS['w1_erroneous'] = W1Thermometer(",
    #                 "    name='w1_erroneous',",
    #                 "    description='Some Thermometer',",
    #                 "    path='/a/b/00-00000000')"
    #             ])

    #         with pydbus.SessionBus() as bus, services.Controller([error_service, thermometer_service]):
    #             self.__wait_error_occurred()
    #             errors = self.__error_client.get_errors()
    #             self.assertEqual(len(errors), 1)

    #             w1_error = errors[0]
    #             self.assertIsInstance(w1_error, DBusHeatingError)
    #             self.assertEqual(w1_error.details['category'], 'w1')
    #             self.assertIn('message', w1_error.details)

    #             w1_specifics = w1_error['w1']
    #             self.assertEqual(w1_specifics['name'], 'w1_erroneous')
    #             self.assertEqual(w1_specifics['issue'], 'file not found')
    #             self.assertEqual(w1_specifics['file'], '/a/b/00-00000000')
    #     except:
    #         print('error >>>\n', error_service.indented_stderr(), '<<<', file=sys.stderr)
    #         print('thermometer >>>\n', thermometer_service.indented_stderr(), '<<<', file=sys.stderr)
    #         raise

    def _error_client(self):
        if self.__error_client is None:
            self.__error_client = Errors_Client(self.__bus)
        return self.__error_client

    def __wait_error_occurred(self):
        with pydbus.SessionBus() as bus:
            client = Errors_Client(bus)
            for _ in range(10):
                nerrors = client.num_errors()
                if nerrors > 0:
                    break
                time.sleep(0.2)
            else:
                self.fail('error count still 0')


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ErrorServiceTest))

if __name__ == '__main__':
    testutils.run(suite)
