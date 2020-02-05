import unittest


def run(suite):
    runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
    runner.run(suite)

