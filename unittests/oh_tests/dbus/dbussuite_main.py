from openheating.test import services
from openheating.test import testutils

import unittest


class MainTest(services.ServiceTestCase):
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MainTest))

if __name__ == '__main__':
    testutils.run(suite)

