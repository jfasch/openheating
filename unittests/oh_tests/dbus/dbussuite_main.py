from openheating.plant import plant
from openheating.plant import config
from openheating.plant.service import PollWitnessService, MainService

from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils

import unittest


class MainTest(PlantTestCase):
    def setUp(self):
        super().setUp()

        self.__poll_witness_file = self.tempfile(suffix='.poll-witness')
        self.__plant_config_file = self.tempfile(
            lines=[
                'from openheating.plant.service import PollWitnessService',
                'ADD_SERVICE(PollWitnessService(witness="{}"))'.format(self.__poll_witness_file.name),
            ],
            suffix='.plant-config')


    @PlantTestCase.intercept_failure
    def test__poll_main__check_witness__manual(self):
        # here we start a plant that corresponds to the plant
        # config. we do this manually, by replicating what's in the
        # config, and adding a main component on top of it.
        self.start_plant(plant.Plant(
            [
                PollWitnessService(witness=self.__poll_witness_file.name),
                MainService(config=self.__plant_config_file.name),
            ]
        ))

        self.poll_main(timestamp=0)

        with open(self.__poll_witness_file.name) as f:
            s = f.read()
            timestamp = int(s)
            self.assertEqual(timestamp, 0)

    def test__poll_main__check_witness__automatic(self):
        # use a helper routine that creates a service list from the
        # plant config, adding all boilerplate like a main component
        # automatically
        the_plant = plant.create_plant_with_main(self.__plant_config_file.name)
        self.start_plant(the_plant)

        self.poll_main(timestamp=0)

        with open(self.__poll_witness_file.name) as f:
            s = f.read()
            timestamp = int(s)
            self.assertEqual(timestamp, 0)


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MainTest))

if __name__ == '__main__':
    testutils.run(suite)
