from openheating.test import testutils
from openheating.test.plant_testcase import PlantTestCase

import unittest


class MainTest(PlantTestCase):
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MainTest))

if __name__ == '__main__':
    testutils.run(suite)

