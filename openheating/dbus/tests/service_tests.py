from openheating.testutils.dbus_testcase import DBusTestCase
from openheating.testutils.switch import TestSwitch
from openheating.dbus.service import DBusService
from openheating.dbus.rebind import DBusClientConnection
from openheating.dbus.thermometer_client import DBusThermometer
from openheating.dbus.switch_client import DBusSwitch
from openheating.dbus.switch_center_client import DBusSwitchCenter
from openheating.dbus.thermometer_center_client import DBusThermometerCenter

from openheating.dbus.service import TestThermometerCreator
from openheating.dbus.service import HWMON_I2C_ThermometerCreator
from openheating.dbus.service import DBusThermometerCreator
from openheating.dbus.service import TestSwitchCreator
from openheating.dbus.service import GPIOSwitchCreator
from openheating.dbus.service import DBusSwitchCreator
from openheating.dbus.service import ThermometerCenterCreator
from openheating.dbus.service import SwitchCenterCreator

from openheating.dbus.service_config import DBusServicesConfig

import time
import signal
import unittest


class ServiceTest(DBusTestCase):
    def setUp(self):
        super().setUp()
        self.__services = []

    def tearDown(self):
        for s in self.__services:
            s.stop()
        super().tearDown()

    def test__single_service(self):
        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={
                '/path/to/test1': TestThermometerCreator(initial_temperature=1),
                '/path/to/test2': TestThermometerCreator(initial_temperature=2),
            })

        self.__services.append(service)

        service.start()

        self.wait_for_object(name='some.dbus.service', path='/path/to/test1')
        self.wait_for_object(name='some.dbus.service', path='/path/to/test2')

        connection = DBusClientConnection(address=self.daemon_address())
        test1_proxy = DBusThermometer(connection=connection, name='some.dbus.service', path='/path/to/test1')
        test2_proxy = DBusThermometer(connection=connection, name='some.dbus.service', path='/path/to/test2')

        self.assertAlmostEqual(test1_proxy.temperature(), 1)
        self.assertAlmostEqual(test2_proxy.temperature(), 2)

        service.stop()

    def test__instantiate_all_objects(self):
        # instantiate all of the different object types in a single
        # service, for the purpose of ensuring everything is
        # there. this way we can make sure no symbol errors occur late
        # at the plant.
        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={
                '/thermometers/test': TestThermometerCreator(initial_temperature=1),
                '/thermometers/i2c': HWMON_I2C_ThermometerCreator(bus_number=666, address=0x49),
                '/thermometers/dbus': DBusThermometerCreator(name='a.b.c', path='/some/thermometer'),
                '/switches/test': TestSwitchCreator(name='testswitch', initial_state=TestSwitch.OPEN),
                # not easily instantiated ... '/switches/gpio': GPIOSwitchCreator(gpio_number=66),
                '/switches/dbus': DBusSwitchCreator(name='a.b.c', path='/some/switch'),
                '/center/thermometers': ThermometerCenterCreator(
                    cache_age=5,
                    thermometers={
                        'test': TestThermometerCreator(initial_temperature=42),
                        'i2c': HWMON_I2C_ThermometerCreator(bus_number=1, address=0x49),
                        'dbus': DBusThermometerCreator(name='a.b.c', path='/x/y/z'),
                    }),
                '/center/switches': SwitchCenterCreator(
                    switches={
                        'test': TestSwitchCreator(name='testswitch', initial_state=TestSwitch.OPEN),
                        'dbus': DBusSwitchCreator(name='a.b.c', path='/some/where'),
                    }),
            })

        self.__services.append(service)

        service.start()
        self.wait_for_object(name='some.dbus.service', path='/thermometers/test')

        # now talk to them
        if True:
            thermometer = DBusThermometer(connection=DBusClientConnection(address=self.daemon_address()),
                                          name='some.dbus.service',
                                          path='/thermometers/test')
            self.assertAlmostEqual(thermometer.temperature(), 1)

        if True:
            switch = DBusSwitch(connection=DBusClientConnection(address=self.daemon_address()),
                                name='some.dbus.service',
                                path='/switches/test')
            self.assertEqual(switch.get_state(), TestSwitch.OPEN)
            switch.do_close()
            self.assertEqual(switch.get_state(), TestSwitch.CLOSED)

        if True:
            thermometer_center = DBusThermometerCenter(connection=DBusClientConnection(address=self.daemon_address()),
                                                       name='some.dbus.service',
                                                       path='/center/thermometers')
            self.assertAlmostEqual(thermometer_center.temperature('test'), 42)

        if True:
            switch_center = DBusSwitchCenter(connection=DBusClientConnection(address=self.daemon_address()),
                                             name='some.dbus.service',
                                             path='/center/switches')
            self.assertEqual(switch_center.get_state('test'), TestSwitch.OPEN)
            switch_center.set_state('test', TestSwitch.CLOSED)
            switch_proxy = switch_center.get_switch('test')
            switch_proxy.do_close()
            self.assertEqual(switch_center.get_state('test'), TestSwitch.CLOSED)

        service.stop()

    def test__servicelist_from_config(self):
        config = DBusServicesConfig(_config % self.daemon_address())
        service_list = config.services()
        self.__services.extend(service_list)
        for s in service_list:
            s.start()

        self.wait_for_object(name='some.service.centers', path='/path/to/switch_center')
        self.wait_for_object(name='some.service.centers', path='/another/path/to/thermometer_center')
        self.wait_for_object(name='some.service.thermometers', path='/path/to/thermometers/i2c')
        self.wait_for_object(name='some.service.thermometers', path='/path/to/thermometers/dbus')
        self.wait_for_object(name='some.service.thermometers', path='/path/to/thermometers/test')
        # not easily instantiated ... self.wait_for_object(name='some.service.switches', path='/path/to/switches/gpio')
        self.wait_for_object(name='some.service.switches', path='/path/to/switches/dbus')
        self.wait_for_object(name='some.service.switches', path='/path/to/switches/test')


_config = '''
DAEMON_ADDRESS = "%s"

SERVICES = {
    'some.service.centers': {
        '/path/to/switch_center': SwitchCenter(
            switches = {
                "switch-test-closed": TestSwitch(name='xxx', initial_state=CLOSED),
                "switch-test-open": TestSwitch(name='yyy', initial_state=OPEN),
                # ot easily instantiated ... "switch-gpio": GPIOSwitch(gpio_number=4),
                "switch-dbus": DBusSwitch(name="a.b.c", path="/some/path")
            }),
        '/another/path/to/thermometer_center': ThermometerCenter(
            cache_age = 5,
            thermometers = {
                "i2c-thermometer": HWMON_I2C_Thermometer(bus_number=1, address=0x49),
                "dbus-thermometer": DBusThermometer(name="a.b.c", path="/some/path"),
                "test-thermometer": TestThermometer(initial_temperature=4.5),
            }),
    },
    
    'some.service.thermometers': {
        '/path/to/thermometers/i2c': HWMON_I2C_Thermometer(bus_number=1, address=0x48),
        '/path/to/thermometers/dbus': DBusThermometer(name="a.b.c", path="/some/path"),
        '/path/to/thermometers/test': TestThermometer(initial_temperature=42.0),
    },

    'some.service.switches': {
        # not easily instantiated ... '/path/to/switches/gpio': GPIOSwitch(gpio_number=42),
        '/path/to/switches/dbus': DBusSwitch(name="a.b.c", path="/some/path"),
        '/path/to/switches/test': TestSwitch(name='xxx', initial_state=OPEN),
    },
}
'''


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ServiceTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
