from openheating.plant.plant import Plant
from openheating.plant.service_def import CrashTestDummyService
from openheating.plant.service_runner import BusnameTimeout

from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils

import unittest


class CrashingServiceTest(PlantTestCase):
    '''We capture stderr of services that are run by a testcase, and print
    it when the testcase fails. Things can go wrong in many ways -
    this is "testing the tests" so to say.

    '''

    @PlantTestCase.intercept_failure
    def test__busname_does_not_appear(self):
        with self.assertRaises(BusnameTimeout):
            self.start_plant(Plant([CrashTestDummyService(no_busname=True)]))

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CrashingServiceTest))

if __name__ == '__main__':
    testutils.run(suite)

