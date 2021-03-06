#!/usr/bin/python3

import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))

from openheating.unittests.easy_suite import suite

import unittest
import logging

logging.getLogger().addHandler(logging.NullHandler())


runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
runner.run(suite)
