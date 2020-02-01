from openheating.base.error import HeatingError

from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.dbus import node
from openheating.dbus.errors import Errors_Client

from openheating.testutils import testutils
from openheating.testutils.plant_testcase import PlantTestCase
from openheating.plant import service
from openheating.plant.plant import Plant

import unittest
import subprocess
import time
import sys


class ErrorsTest(PlantTestCase):

    @PlantTestCase.intercept_failure
    def test__basic_error_count(self):
        thermometers_config = self.tempfile(
            lines=[
                "from openheating.base.thermometer import ErrorThermometer",
                "ADD_THERMOMETER('Error', 'Error Thermometer', ErrorThermometer(n_ok_before_error=0)),",
            ],
            suffix='.thermometers-config',
        )

        self.start_plant(
            plant=Plant([
                service.ErrorService(),
                service.ThermometerService(config=thermometers_config.name),                    
            ]),
            thermometer_background_updates=False,
        )
        
        client = Errors_Client(self.bus)
        self.__wait_error_occurred(client)

    @PlantTestCase.intercept_failure
    def test__w1__file_not_found(self):
        thermometers_config = self.tempfile(
            lines=[
                "from openheating.base.w1 import W1Thermometer",
                "ADD_THERMOMETER('w1_erroneous', 'Some Thermometer', W1Thermometer(path='/a/b/00-00000000')),",
            ],
            suffix='.thermometers-config',
        )

        self.start_plant(
            plant=Plant([
                service.ErrorService(),
                service.ThermometerService(config=thermometers_config.name),
            ]),
            # "background updates" make thermometer service read
            # temperatures at startup.
            thermometer_background_updates=True,
        )

        client = Errors_Client(self.bus)
        self.__wait_error_occurred(client)
        errors = client.get_errors()
        self.assertEqual(len(errors), 1)

        w1_error = errors[0]
        self.assertIsInstance(w1_error, node.DBusHeatingError)
        self.assertEqual(w1_error.details['category'], 'w1')
        self.assertIn('message', w1_error.details)

        w1_specifics = w1_error.details['w1']
        self.assertEqual(w1_specifics['issue'], 'file read error')
        self.assertEqual(w1_specifics['file'], '/a/b/00-00000000/w1_slave')

    def __wait_error_occurred(self, client):
        for _ in range(10):
            nerrors = client.num_errors()
            if nerrors > 0:
                break
            time.sleep(0.2)
        else:
            self.fail('error count still 0')


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ErrorsTest))

if __name__ == '__main__':
    testutils.run(suite)
