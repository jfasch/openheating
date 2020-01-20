from openheating.base.error import HeatingError
from openheating.base.thermometer import FileThermometer

from openheating.testutils import testutils
from openheating.testutils.plant_testcase import PlantTestCase
from openheating.plant import service
from openheating.plant.plant import Plant

from openheating.dbus.thermometer_center import ThermometerCenter_Client

import os.path
import unittest


class ThermometersOK(PlantTestCase):
    def setUp(self):
        super().setUp()
        config = self.tempfile(
            lines=[
                "from openheating.base.thermometer import InMemoryThermometer",
                "ADD_THERMOMETER('TestThermometer', 'Test Thermometer', InMemoryThermometer(42))",
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

    def test__start_stop(self):
        center_client = ThermometerCenter_Client(self.bus)
        thermometer_client = center_client.get_thermometer('TestThermometer')
        self.assertEqual(thermometer_client.get_name(), 'TestThermometer')
        self.assertEqual(thermometer_client.get_description(), 'Test Thermometer')
        self.assertAlmostEqual(thermometer_client.get_temperature(), 42)

    def test__get_temperature(self):
        center_client = ThermometerCenter_Client(self.bus)
        thermometer_client = center_client.get_thermometer('TestThermometer')
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
                "ADD_THERMOMETER('ErrorThermometer', 'Error Thermometer', ErrorThermometer(n_ok_before_error = False))",
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

    def test__sensor_error_at_startup(self):
        # do nothing. this is only there to test if startup succeeds
        # when a sensor returns an error initially.
        pass

    def test__client_error(self):
        center_client = ThermometerCenter_Client(self.bus)
        thermometer_client = center_client.get_thermometer('ErrorThermometer')
        self.assertRaises(HeatingError, thermometer_client.get_temperature)

class ThermometersSimulation(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__tmpdir = self.tempdir()

    def tearDown(self):
        super().tearDown()

    def test__simulated_thermometers_dir__passed(self):
        thdir = self.__tmpdir.name+'/some/dir/to/contain/thermometers'
        config=self.tempfile(
            lines=[
                'assert GET_SIMULATED_THERMOMETERS_DIR() == "{}"'.format(thdir)
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant(
            [
                service.ThermometerService(
                    config=config.name,
                    simulated_thermometers_dir=thdir
                ),
            ]
        ))

        self.assertTrue(os.path.isdir(thdir)) # has been created by service

    def test__simulated_thermometers_dir__not_passed(self):
        config=self.tempfile(
            lines=[
                'assert GET_SIMULATED_THERMOMETERS_DIR() is None',
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

    def test__force_update_of_file_thermometer(self):
        # usually thermometer updates are done by the thermometer
        # service in the background, every 5s or so. this is ok for
        # live operation, but not really helpful in tests where we
        # have our own virtualized time axis.

        test_thermometer_path = self.__tmpdir.name + '/test-thermometer'

        config=self.tempfile(
            lines=[
                'from openheating.base.thermometer import FileThermometer',
                'ADD_THERMOMETER("test", "test", FileThermometer(path="{}", initial_value=20))'.format(test_thermometer_path),
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name, 
                                                           # jjj: move
                                                           # to
                                                           # PlantTestCase
                                                           background_updates=False)]))

        # paranoia: see if thermometer is there, and it has the
        # configured initial temperature value
        center_client = ThermometerCenter_Client(self.bus)
        self.assertIn('test', center_client.all_names())

        test_thermometer_client = center_client.get_thermometer('test')

        # jjj move to PlantTestCase, right after plant startup
        test_thermometer_client.force_update(timestamp=0)

        self.assertAlmostEqual(test_thermometer_client.get_temperature(), 20)

        # modify temperature by writing to the file
        test_thermometer = FileThermometer(path=test_thermometer_path)
        test_thermometer.set_temperature(30)

        test_thermometer_client.force_update(0)

        self.assertAlmostEqual(test_thermometer_client.get_temperature(), 30)
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersOK))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersError))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersSimulation))

if __name__ == '__main__':
    testutils.run(suite)
