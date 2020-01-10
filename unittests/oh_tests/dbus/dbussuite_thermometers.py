from openheating.base.error import HeatingError

from openheating.testutils import testutils
from openheating.testutils.plant_testcase import PlantTestCase
from openheating.plant import service
from openheating.plant.plant import Plant

from openheating.dbus import dbusutil
from openheating.dbus.thermometer_center import ThermometerCenter_Client

import pydbus

import os.path
import unittest


class ThermometersOK(PlantTestCase):
    def setUp(self):
        super().setUp()
        config = self.tempfile(
            lines=[
                "from openheating.base.thermometer import FixedThermometer",
                "ADD_THERMOMETER(FixedThermometer('TestThermometer', 'Test Thermometer', 42))",
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

    def test__start_stop(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('TestThermometer')
        self.assertEqual(thermometer_client.get_name(), 'TestThermometer')
        self.assertEqual(thermometer_client.get_description(), 'Test Thermometer')
        self.assertAlmostEqual(thermometer_client.get_temperature(), 42)

    def test__get_temperature(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('TestThermometer')
        self.assertAlmostEqual(thermometer_client.get_temperature(), 42)

    def test__list(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        all_names = center_client.all_names()
        self.assertEqual(len(all_names), 1)
        self.assertIn('TestThermometer', all_names)

    def test__inject_sample__not_possible(self):
        # we are running periodic updates, so it must not be possible
        # to inject samples
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('TestThermometer')
        try:
            thermometer_client.inject_sample(timestamp=666, temperature=42)
            self.fail()
        except HeatingError as e:
            self.assertIn('tag', e.details)
            self.assertEqual(e.details['tag'], 'INJECT_WHILE_BACKGROUND_UPDATE')


class ThermometersInjectSamples(PlantTestCase):
    def setUp(self):
        super().setUp()
        config=self.tempfile(
            lines=[
                "from openheating.base.thermometer import DummyThermometer",
                "ADD_THERMOMETER(DummyThermometer('TestThermometer', 'Test Thermometer', 42))",
                # no updates; else injecting won't work
                "SET_UPDATE_INTERVAL(0)",
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

    def test__inject_sample(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('TestThermometer')
        thermometer_client.inject_sample(timestamp=0, temperature=20)
        self.assertAlmostEqual(thermometer_client.get_temperature(), 20)

class ThermometersError(PlantTestCase):
    def setUp(self):
        super().setUp()
        config=self.tempfile(
            lines=[
                "from openheating.base.thermometer import ErrorThermometer",
                "ADD_THERMOMETER(ErrorThermometer('ErrorThermometer', 'Error Thermometer', n_ok_before_error = False))",
            ],
            suffix='.thermometers-config',
        )
        self.start_plant(Plant([service.ThermometerService(config=config.name)]))

    def test__sensor_error_at_startup(self):
        # do nothing. this is only there to test if startup succeeds
        # when a sensor returns an error initially.
        pass

    def test__client_error(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
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

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersOK))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersInjectSamples))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersError))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersSimulation))

if __name__ == '__main__':
    testutils.run(suite)
