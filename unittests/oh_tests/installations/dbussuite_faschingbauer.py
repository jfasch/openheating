from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils
from openheating.plant import locations
from openheating.plant.plant import Plant, create_plant_with_main
from openheating.plant.service_def import ThermometerService
from openheating.plant.service_def import SwitchService
from openheating.plant.service_def import CircuitService
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
            ThermometerService(config=locations.confdir + '/thermometers.pyconf'),
            SwitchService(config=locations.confdir + '/switches.pyconf'),
            CircuitService(config=locations.confdir + '/circuits.pyconf'),
        ]))

    @PlantTestCase.intercept_failure
    def test__run_plant(self):
        self.start_plant(create_plant_with_main(
            locations.confdir + '/plant.pyconf'))

        thermometer_center = ThermometerCenter_Client(self.bus)
        self.assertIn('Raum', thermometer_center.all_names())

        switch_center = SwitchCenter_Client(self.bus)
        self.assertIn('ww', switch_center.all_names())

        circuit_center = CircuitCenter_Client(self.bus)
        self.assertIn('ww', circuit_center.all_names())
        
    @PlantTestCase.intercept_failure
    def test__manual_poll(self):
        self.start_plant(create_plant_with_main(locations.confdir + '/plant.pyconf'))

        # hmmm. "no background updates" means that temperature is not
        # initially read. is this really necessary?
        self.force_temperature_update(timestamp=next(self.__timeline))

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

