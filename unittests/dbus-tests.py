#!/usr/bin/python3

import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))

from openheating.dbus.unittests.dbus_suite import suite as dbus_suite

import unittest
import logging


logging.getLogger().addHandler(logging.NullHandler())

suite = unittest.TestSuite()
suite.addTest(dbus_suite)

runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
runner.run(suite)
