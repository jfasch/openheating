from openheating.plant.plant import Plant
from openheating.plant.service import CrashTestDummyService, BusnameTimeout

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
            self.start_plant(
                plant=Plant([
                    CrashTestDummyService(no_busname=True),
                ]),
                thermometer_background_updates=False,                            
            )

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CrashingServiceTest))

if __name__ == '__main__':
    testutils.run(suite)

