#!/usr/bin/python

import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))

from heating.tests.suite import suite

import unittest


runner = unittest.TextTestRunner()
runner.run(suite)
