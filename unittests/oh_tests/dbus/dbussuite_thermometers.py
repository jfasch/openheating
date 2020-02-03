from openheating.base.error import HeatingError
from openheating.base.thermometer import FileThermometer

from openheating.testutils import testutils
from openheating.testutils.plant_testcase import PlantTestCase
from openheating.plant import service
from openheating.plant.plant import Plant

from openheating.dbus.thermometer_center import ThermometerCenter_Client

import os.path
import itertools
import unittest


class ThermometersOK(PlantTestCase):
    def setUp(self):
        super().setUp()
        config = self.tempfile(
            lines=[
                "from openheating.base.thermometer import InMemoryThermometer",
                "ADD_THERMOMETER('TestThermometer', 'Test Thermometer', None)",
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

    def test__start_stop(self):
        # inject the temperature we want into the simulation file.
        self.set_temperature_file_and_update('TestThermometer', 42, timestamp=666)

        center_client = ThermometerCenter_Client(self.bus)
        thermometer_client = center_client.get_thermometer('TestThermometer')
        self.assertEqual(thermometer_client.get_name(), 'TestThermometer')
        self.assertEqual(thermometer_client.get_description(), 'Test Thermometer')
        self.assertAlmostEqual(thermometer_client.get_temperature(), 42)

    def test__list(self):
        center_client = ThermometerCenter_Client(self.bus)
        all_names = center_client.all_names()
        self.assertEqual(len(all_names), 1)
        self.assertIn('TestThermometer', all_names)

class ThermometersError(PlantTestCase):
    def setUp(self):
        super().setUp()
        config=self.tempfile(
            lines=[
                "from openheating.base.thermometer import ErrorThermometer",
                "ADD_THERMOMETER('ErrorThermometer', 'Error Thermometer', ErrorThermometer, n_ok_before_error = False)",
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(
            Plant([service.ThermometerService(config=config.name)]),
            simulation=False, # so ErrorThermometer is taken as specified
        )

    def test__sensor_error_at_startup(self):
        # do nothing. this is only there to test if startup succeeds
        # when a sensor returns an error initially.
        pass

    def test__client_error(self):
        center_client = ThermometerCenter_Client(self.bus)
        thermometer_client = center_client.get_thermometer('ErrorThermometer')
        self.assertRaises(HeatingError, thermometer_client.get_temperature)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersOK))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersError))

if __name__ == '__main__':
    testutils.run(suite)
