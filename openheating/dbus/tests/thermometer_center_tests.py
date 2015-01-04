from openheating.dbus.thermometer_center_config import ThermometerCenterConfig
from openheating.dbus.rebind import DBusConnectionProxy
from openheating.thermometer import Thermometer
from openheating.thermometer_center import ThermometerCenter

import unittest

class ThermometerCenterTest(unittest.TestCase):
    def test__configfile(self):
        content = '\n'.join(
            ['DAEMON_ADDRESS = "tcp:host=1.2.3.4,port=6666"',
             'BUS_NAME = "some.arbitrary.name"',

             'PATH = "/my/center"',
             'CACHE_AGE = 5',

             'THERMOMETERS = (',
             '    ("name_1", HWMON_I2C_Thermometer(bus_number=1, address=0x49)),',
             '    ("name_2", DBusThermometer(name="a.b.c", path="/some/path")),',
             '    ("name_3", TestThermometer(initial_temperature=4.5)),',
             ')',
             ])

        config = ThermometerCenterConfig(content)

        self.assertEqual(config.daemon_address(), "tcp:host=1.2.3.4,port=6666")
        self.assertEqual(config.bus_name(), "some.arbitrary.name")

        self.assertEqual(config.path(), "/my/center")
        self.assertAlmostEqual(config.cache_age(), 5)

        thermo_list = list(config.iter_thermometers())
        
        self.assertEqual(len(thermo_list), 3)

        thermo_dict = dict(thermo_list)

        self.assertIn('name_1', thermo_dict)
        self.assertIn('name_2', thermo_dict)
        self.assertIn('name_3', thermo_dict)

        for name, creator in config.iter_thermometers():
            self.assertIsInstance(creator.create(connection_proxy=DBusConnectionProxy('')), Thermometer)

        center = ThermometerCenter(((name, creator.create(DBusConnectionProxy(''))) for name, creator in config.iter_thermometers()))

        self.assertAlmostEqual(center.temperature('name_3'), 4.5)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ThermometerCenterTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
