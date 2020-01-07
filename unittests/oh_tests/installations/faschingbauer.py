from openheating.test.plant_testcase import PlantTestCase
from openheating.test import testutils

import unittest


class FaschingbauerTest(PlantTestCase):
    def test__basic(self):
        #self.fail()
        pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(FaschingbauerTest))

if __name__ == '__main__':
    testutils.run(suite)

