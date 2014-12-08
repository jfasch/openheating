#!/usr/bin/python3

import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))

from openheating.tests.raspi_suite import suite

import unittest


runner = unittest.TextTestRunner()
runner.run(suite)
