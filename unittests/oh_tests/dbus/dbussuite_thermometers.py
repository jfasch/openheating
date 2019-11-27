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
                "THERMOMETERS['TestThermometer'] = FixedThermometer('TestThermometer', 'Test Thermometer', 42)",
                ])
        ])

    def test__start_stop(self):
        center_client = ThermometerCenter_Client(pydbus.SessionBus())
        thermometer_client = center_client.get_thermometer('TestThermometer')
        self.assertEqual(thermometer_client.get_name(), 'TestThermometer')
        self.assertEqual(thermometer_client.get_description(), 'Test Thermometer')
        self.assertAlmostEqual(thermometer_client.get_temperature(), 42)

    def test__thermometer_client_prog__current(self):
        completed_process = subprocess.run(
            [testutils.find_executable('openheating-thermometer-client.py'), '--session', 'current', 'TestThermometer'],
            stdout=subprocess.PIPE, check=True, universal_newlines=True)
        temperature = eval(completed_process.stdout)
        self.assertAlmostEqual(temperature, 42)

    def test__thermometer_client_prog__list(self):
        completed_process = subprocess.run(
            [testutils.find_executable('openheating-thermometer-client.py'), '--session', 'list'], 
            stdout=subprocess.PIPE, check=True, universal_newlines=True)
        thermometers = [name for name in completed_process.stdout.split('\n') if name != '']
        self.assertEqual(len(thermometers), 1)
        self.assertIn('TestThermometer', thermometers)


class ThermometersError(services.ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.start_services([
            services.ThermometerService(pyconf=[
                "from openheating.base.thermometer import ErrorThermometer",
                "THERMOMETERS['ErrorThermometer'] = ErrorThermometer('ErrorThermometer', 'Error Thermometer', n_ok_before_error = False)",
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
