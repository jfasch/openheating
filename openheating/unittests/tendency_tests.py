from openheating.tendency import Tendency

import unittest
import logging


class TendencyTest(unittest.TestCase):
    def test__basic(self):
        tendency = Tendency()

        self.assertTrue(tendency.even())

        tendency.add(20)
        self.assertTrue(tendency.even())

        tendency.add(21)
        self.assertTrue(tendency.rising())

        tendency.add(21)
        self.assertTrue(tendency.rising())

        tendency.add(21)
        self.assertTrue(tendency.rising())

        tendency.add(21)
        self.assertTrue(tendency.even())

        tendency.add(20)
        self.assertTrue(tendency.even())
        
        tendency.add(10)
        self.assertTrue(tendency.falling())
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TendencyTest))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
