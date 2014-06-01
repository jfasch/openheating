from lm73_tests import suite as lm73_suite

import unittest

suite = unittest.TestSuite()

suite.addTest(lm73_suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
