#!/usr/bin/python3

import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))

from oh_tests.base.easysuite import suite as oh_base_suite
from oh_tests.dbus.easysuite import suite as oh_dbus_suite

import unittest
import logging


logging.getLogger().addHandler(logging.NullHandler())

suite = unittest.TestSuite()
suite.addTest(oh_base_suite)
suite.addTest(oh_dbus_suite)

runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
runner.run(suite)
