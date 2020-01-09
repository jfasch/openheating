from openheating.test.plant_testcase import PlantTestCase
from openheating.test import testutils
from openheating.test.plant import Plant
from openheating.test import service

import unittest
import tempfile
import os.path


class FaschingbauerTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__thermometers_dir = tempfile.TemporaryDirectory(suffix='-thermometers')
        self.__switches_dir = tempfile.TemporaryDirectory(suffix='-switches')
    def tearDown(self):
        self.__thermometers_dir.cleanup()
        self.__switches_dir.cleanup()
        super().tearDown()

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
        self.fail('PlantRunner service')


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FaschingbauerTest))

if __name__ == '__main__':
    testutils.run(suite)

