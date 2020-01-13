from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils
from openheating.plant.plant import Plant
from openheating.plant import service

import unittest
import os.path


class FaschingbauerTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__thermometers_dir = self.tempdir(suffix='.thermometers')
        self.__switches_dir = self.tempdir(suffix='.switches')

    @PlantTestCase.intercept_failure
    def test__basic(self):
        self.start_plant(Plant([
            service.ThermometerService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'thermometers.pyconf'),
                simulated_thermometers_dir=self.__thermometers_dir.name),
            service.SwitchService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'switches.pyconf'),
                simulated_switches_dir=self.__switches_dir.name),
            service.CircuitService(
                config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'circuits.pyconf')),
        ]))

    @PlantTestCase.intercept_failure
    def test__run_plant(self):
        # self.start_plant(Plant([
        #     service.PlantRunnerService(
        #         config=os.path.join(testutils.find_project_root(), 'installations', 'faschingbauer', 'plant.pyconf'),
        #         simulated_thermometers_dir=self.__thermometers_dir.name,
        #         simulated_switches_dir=self.__switches_dir.name),
        # ]))

        # thermometer_center = ThermometerCenter_Client(

        pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FaschingbauerTest))

if __name__ == '__main__':
    testutils.run(suite)

