from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils
from openheating.plant.plant import Plant
from openheating.plant import service
from openheating.dbus.thermometer_center import ThermometerCenter_Client
from openheating.dbus.switch_center import SwitchCenter_Client

import unittest
import os.path
import signal


class FaschingbauerTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__simulated_dir = self.tempdir(suffix='.simulated')
        self.__thermometers_dir = self.__simulated_dir.name + '/thermometers'
        self.__switches_dir = self.__simulated_dir.name + '/switches'

    @PlantTestCase.intercept_failure
    def test__basic(self):
        self.start_plant(Plant([
            service.ThermometerService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'thermometers.pyconf'),
                simulation_dir=self.__thermometers_dir),
            service.SwitchService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'switches.pyconf'),
                simulated_switches_dir=self.__switches_dir),
            service.CircuitService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'circuits.pyconf')),
        ]))

    @PlantTestCase.intercept_failure
    def test__run_plant(self):
        self.start_plant(Plant([
            service.PlantRunnerService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'plant.pyconf'),
                simulated_dir=self.__simulated_dir.name),
        ]))

        thermometer_center = ThermometerCenter_Client(self.bus)
        self.assertIn('Raum', thermometer_center.all_names())

        switch_center = SwitchCenter_Client(self.bus)
        self.assertIn('ww', switch_center.all_names())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FaschingbauerTest))

if __name__ == '__main__':
    testutils.run(suite)

