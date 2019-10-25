from .asyncio_suite import suite as asyncio_suite
from .history import suite as history_suite
from .thermometer_test import suite as thermometer_suite
from .thermometers_conf import suite as thermometers_conf_suite
from .switches_ini import suite as switches_ini_suite

import unittest


suite = unittest.TestSuite()

suite.addTest(asyncio_suite)
suite.addTest(history_suite)
suite.addTest(thermometer_suite)
suite.addTest(thermometers_conf_suite)
suite.addTest(switches_ini_suite)
