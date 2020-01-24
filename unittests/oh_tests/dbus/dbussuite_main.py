from openheating.plant.plant import Plant
from openheating.plant.service import PollWitnessService, MainService

from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils

import unittest


class MainTest(PlantTestCase):
    @PlantTestCase.intercept_failure
    def test__poll_main__check_witness(self):
        poll_witness = self.tempfile(suffix='.poll-witness')
        plant_config = self.tempfile(
            lines=[
                'from openheating.plant.service import PollWitnessService',
                'ADD_SERVICE(PollWitnessService(witness="{}"))'.format(poll_witness.name),
            ],
            suffix='.plant-config')

        self.start_plant(Plant(
            [
                PollWitnessService(witness=poll_witness.name),
                MainService(config=plant_config.name),
            ]
        ))

        self.poll_main(timestamp=0)

        with open(poll_witness.name) as f:
            s = f.read()
            timestamp = int(s)
            self.assertEqual(timestamp, 0)


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MainTest))

if __name__ == '__main__':
    testutils.run(suite)

