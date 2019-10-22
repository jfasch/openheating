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


class ErrorServiceTest(unittest.TestCase):
    def setUp(self):
        self.__thermometer_service = services.ThermometerService(pyconf=[
            "from openheating.thermometer import ErrorThermometer",
            "THERMOMETERS['Error'] = ErrorThermometer(",
            "    name='Error',",
            "    descriptior='Error Thermometer',",
            "    n_ok_before_error=0)"
        ])
        self.__error_service = services.ErrorService()

        services.start((
            # error service starts first so it can see the errors
            self.__error_service, 
            self.__thermometer_service))

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
