from openheating.base.error import HeatingError

from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.thermometer_center import ThermometerCenter_Client

import pydbus

import unittest
import subprocess


class ThermometersOK(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.start_services([
            services.ThermometerService(pyconf=[
                "from openheating.base.thermometer import FixedThermometer",
                "THERMOMETERS = [FixedThermometer('TestThermometer', 'Test Thermometer', 42)]",
                ])
        ])

    def test__start_stop(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('TestThermometer')
        self.assertEqual(thermometer_client.get_name(), 'TestThermometer')
        self.assertEqual(thermometer_client.get_description(), 'Test Thermometer')
        self.assertAlmostEqual(thermometer_client.get_temperature(), 42)

    def test__get_temperature(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('TestThermometer')
        self.assertAlmostEqual(thermometer_client.get_temperature(), 42)

    def test__list(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        all_names = center_client.all_names()
        self.assertEqual(len(all_names), 1)
        self.assertIn('TestThermometer', all_names)
    

class ThermometersError(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.start_services([
            services.ThermometerService(pyconf=[
                "from openheating.base.thermometer import ErrorThermometer",
                "THERMOMETERS = [ErrorThermometer('ErrorThermometer', 'Error Thermometer', n_ok_before_error = False)]",
            ])
        ])

    def test__sensor_error_at_startup(self):
        # do nothing. this is only there to test if startup succeeds
        # when a sensor returns an error initially.
        pass

    def test__client_error(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('ErrorThermometer')
        self.assertRaises(HeatingError, thermometer_client.get_temperature)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersOK))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometersError))

if __name__ == '__main__':
    testutils.run(suite)
