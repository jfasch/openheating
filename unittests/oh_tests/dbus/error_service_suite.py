from openheating.error import HeatingError

from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.errors import Errors_Client

import pydbus

import unittest
import subprocess
import time


class ErrorServiceTest(unittest.TestCase):
    def setUp(self):
        self.__thermometer_service = services.ThermometerService(ini=[
            '[Error]',
            'Type = error',
            'Description = Error Thermometer',
            'NOkBeforeError = 0'])
        self.__error_service = services.ErrorService()

        services.start((self.__thermometer_service, self.__error_service))

    def tearDown(self):
        services.stop((self.__thermometer_service, self.__error_service))
        
    def test__basic_error_count(self):
        with pydbus.SessionBus() as bus:
            errclient = Errors_Client(bus)
            for _ in range(10):
                nerrors = errclient.num_errors()
                if nerrors > 0:
                    break
                time.sleep(0.2)
            else:
                self.fail('error count still 0')

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ErrorServiceTest))

if __name__ == '__main__':
    testutils.run(suite)
