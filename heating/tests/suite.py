from .transport_tests import suite as transport_suite

import unittest

suite = unittest.TestSuite()
suite.addTest(transport_suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
