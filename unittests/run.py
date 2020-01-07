#!/usr/bin/python3

import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))

from oh_tests.base.easysuite import suite as oh_base_easysuite
from oh_tests.dbus.easysuite import suite as oh_dbus_easysuite
from oh_tests.dbus.dbussuite import suite as oh_dbus_dbussuite
from oh_tests.installations.faschingbauer import suite as oh_installations_faschingbauer_suite

import unittest
import logging


logging.getLogger().addHandler(logging.NullHandler())

suite = unittest.TestSuite()
suite.addTest(oh_base_easysuite)
suite.addTest(oh_dbus_easysuite)
suite.addTest(oh_dbus_dbussuite)
suite.addTest(oh_installations_faschingbauer_suite)

runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
runner.run(suite)
