from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils
from openheating.plant.plant import Plant, create_plant_with_main
from openheating.plant import service
from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.dbus.switch_center import SwitchCenter_Client
from openheating.dbus.circuit_center import CircuitCenter_Client
from openheating.dbus.main import MainPollable_Client

import unittest
import os.path
import signal
import itertools


class FaschingbauerTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__simulation_dir = self.tempdir(suffix='.simulation')
        self.__thermometers_dir = self.__simulation_dir.name + '/thermometers'
        self.__switches_dir = self.__simulation_dir.name + '/switches'

        self.__timeline = itertools.count()

    @PlantTestCase.intercept_failure
    def test__basic(self):
        # run the plant components directly (simply to check if the
        # basis is ok before we start hammering on it running as a
        # compound system).

        self.start_plant(Plant([
            service.ThermometerService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'thermometers.pyconf'),
                simulation_dir=self.__thermometers_dir),
            service.SwitchService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'switches.pyconf'),
                simulation_dir=self.__switches_dir),
            service.CircuitService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'circuits.pyconf')),
        ]))

    @PlantTestCase.intercept_failure
    def test__run_plant(self):
        self.start_plant(
            create_plant_with_main(
                os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'plant.pyconf'),
                simulation_dir=self.__simulation_dir.name,
                thermometer_center
))

        thermometer_center = ThermometerCenter_Client(self.bus)
        self.assertIn('Raum', thermometer_center.all_names())

        switch_center = SwitchCenter_Client(self.bus)
        self.assertIn('ww', switch_center.all_names())

        circuit_center = CircuitCenter_Client(self.bus)
        self.assertIn('ww', circuit_center.all_names())
        
    @PlantTestCase.intercept_failure
    def test__manual_poll(self):
        self.start_plant(
            plant=create_plant_with_main(
                os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'plant.pyconf'),
                simulation_dir=self.__simulation_dir.name),
            thermometer_background_updates=False,
        )

        # paranoia: verify initial state. ("20" is set in the
        # thermometer config code when simulation is wanted. probably
        # not the best idea.)
        self.assertAlmostEqual(self.get_temperature_dbus('SpeicherOben'), 20)
        self.assertAlmostEqual(self.get_temperature_dbus('Holzbrenner'), 20)
        self.assertFalse(self.get_switchstate_dbus('ww'))
        self.assertFalse(self.is_circuit_active('ww'))

        # activate circuit, and poll. no effect (no temperature
        # difference).
        self.activate_circuit('ww')
        self.poll_main(next(self.__timeline))
        self.assertFalse(self.get_switchstate_file('ww'))
        
        # set holz temperature, poll again, effect
        self.set_temperature_file_and_update('Holzbrenner', 40, timestamp=next(self.__timeline))
        self.poll_main(next(self.__timeline))
        self.assertTrue(self.get_switchstate_file('ww'))


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FaschingbauerTest))

if __name__ == '__main__':
    testutils.run(suite)

