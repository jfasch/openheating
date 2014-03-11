import unittest

class TransportTest(unittest.TestCase):
    def test_basic(self):
        self.fail()

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportTest))
