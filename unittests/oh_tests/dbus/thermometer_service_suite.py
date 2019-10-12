from openheating.test import testutils
from openheating.test import services

from openheating.dbus import dbusutil
from openheating.dbus.thermometer_center import ThermometerCenter_Client

import pydbus

import unittest
import subprocess


class ThermometerServiceOK(unittest.TestCase):
    def setUp(self):
        self.__service = services.ThermometerService(ini=[
            '[TestThermometer]',
            'Type = fixed',
            'Description = Test Thermometer',
            'Value = 42'])

    def tearDown(self):
        self.__service.stop()
        
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


class ThermometerServiceError(unittest.TestCase):
    def setUp(self):
        self.__service = services.ThermometerService(ini=[
            '[ErrorThermometer]',
            'Type = error',
            'Description = Error Thermometer',
            'NOkBeforeError = 0'])

    def tearDown(self):
        self.__service.stop()

    def test__sensor_error_at_startup(self):
        self.fail('how to report success? do nothing?')
        pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerServiceOK))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerServiceError))

if __name__ == '__main__':
    testutils.run(suite)
