from openheating import testutils
from openheating.dbus import dbusutil
from openheating.dbus.thermometer_center import ThermometerCenter_Client

import pydbus

import unittest
import tempfile
import subprocess


class ThermometerServiceTest(unittest.TestCase):
    def setUp(self):
        self.__ini = tempfile.NamedTemporaryFile(mode='w')
        self.__ini.write('\n'.join([
            '[TestThermometer]',
            'Type = fixed',
            'Description = Test Thermometer',
            'Value = 42']))
        self.__ini.flush()
        self.__service = subprocess.Popen([
            testutils.find_executable('openheating-thermometers.py'),
            '--session',
            '--configfile', self.__ini.name,
        ])

        # wait until busname appears
        completed_process = subprocess.run([
            'gdbus', 'wait', '--session', dbusutil.THERMOMETERS_BUSNAME, '--timeout', '10'])
        if completed_process.returncode != 0:
            self.fail()

    def tearDown(self):
        self.__service.terminate()
        # our services mess with signals a bit (graceful eventloop
        # termination), so apply a timeout in case anything goes
        # wrong.
        self.__service.wait(timeout=5) 
        self.__ini.close()

        # wait for busname to disappear
        for _ in range(10):
            completed_process = subprocess.run(
                ['gdbus', 'call', '--session', '--dest', 'org.freedesktop.DBus',
                 '--object-path', '/org/freedesktop/DBus', '--method', 'org.freedesktop.DBus.ListNames'],
                stdout=subprocess.PIPE,
                check=True,
            )
            names = eval(completed_process.stdout)
            
            if dbusutil.THERMOMETERS_BUSNAME in names:
                time.sleep(0.5)
                continue
            else:
                break
        else:
            self.fail('{} still on the bus'.format(dbusutil.THERMOMETERS_BUSNAME))

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

if __name__ == '__main__':
    unittest.main()
else:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerServiceTest)
