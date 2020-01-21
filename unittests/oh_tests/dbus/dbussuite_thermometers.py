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
        self.__timeline = itertools.count()

    def tearDown(self):
        super().tearDown()

    def test__simulated_thermometers_dir__passed(self):
        thdir = self.__tmpdir.name+'/some/dir/to/contain/thermometers'
        config=self.tempfile(
            lines=[
                'from openheating.base.thermometer import InMemoryThermometer',

                # simulation is on. we expect the InMemoryThermometer
                # to be ignored, in favor of an implicitly created
                # FileThermometer instance. that instance is tied to
                # file thdir/test_name which exists after the
                # thermometer service has started.
                'ADD_THERMOMETER("test_name", "test description", InMemoryThermometer(42))',
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant(
            [
                service.ThermometerService(
                    config=config.name,
                    simulation_dir=thdir,
                    background_updates=False,
                ),
            ]
        ))

        self.assertTrue(os.path.isfile(thdir+'/test_name')) # has been created by service

        # modify temperature via PlantTestCase convenience
        # method. that goes to the file, sets the temperature, and
        # forces a temperature update in the thermometer service.
        self.set_temperature_file_and_update(name='test_name', value=7, 
                                             timestamp=next(self.__timeline))

        # again, verify using convenience method. this time regular
        # dbus communication.
        self.assertAlmostEqual(self.get_temperature_dbus('test_name'), 7)

    def test__simulated_thermometers_dir__not_passed(self):
        temperature_file = self.tempfile(suffix='.temperature')
        config=self.tempfile(
            lines=[
                'from openheating.base.thermometer import FileThermometer',

                # simulation is off. we expect the thermometer to be
                # added as-is.
                'ADD_THERMOMETER(',
                '      "test_name", "test description",',
                '      FileThermometer("{}", initial_value=42))'.format(temperature_file.name),
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

        # simulation is off, so thermometer must have been taken as-is
        # => file contains the initial value as specified by config.
        file_thermometer = FileThermometer(temperature_file.name)
        self.assertAlmostEqual(file_thermometer.get_temperature(), 42)

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
