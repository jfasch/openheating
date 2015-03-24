from openheating.testutils.dbus_testcase import DBusTestCase
from openheating.dbus.service import DBusService
from openheating.dbus.rebind import DBusClientConnection
from openheating.dbus.thermometer_client import DBusThermometerClient
from openheating.dbus.switch_client import DBusSwitchClient
from openheating.dbus.switch_center_client import DBusSwitchCenterClient
from openheating.dbus.thermometer_center_client import DBusThermometerCenterClient

from openheating.dbus.service import TestThermometerObjectCreator
from openheating.dbus.service import FileThermometerObjectCreator
from openheating.dbus.service import HWMON_I2C_ThermometerObjectCreator
from openheating.dbus.service import DBusThermometerClientObjectCreator
from openheating.dbus.service import TestSwitchObjectCreator
from openheating.dbus.service import FileSwitchObjectCreator
from openheating.dbus.service import GPIOSwitchObjectCreator
from openheating.dbus.service import DBusSwitchClientObjectCreator
from openheating.dbus.service import ThermometerCenterObjectCreator
from openheating.dbus.service import SwitchCenterObjectCreator

from openheating.dbus.service_config import DBusServicesConfig
from openheating.dbus.native_creator import NativeObject

from openheating.testutils.test_thermometer import TestThermometer
from openheating.testutils.test_switch import TestSwitch
from openheating.hardware.thermometer_hwmon import HWMON_I2C_Thermometer

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
                '/path/to/test1': TestThermometerObjectCreator(initial_temperature=1),
                '/path/to/test2': TestThermometerObjectCreator(initial_temperature=2),
            })

        self.__services.append(service)

        service.start()

        self.wait_for_object(name='some.dbus.service', path='/path/to/test1')
        self.wait_for_object(name='some.dbus.service', path='/path/to/test2')

        connection = DBusClientConnection(address=self.daemon_address())
        test1_proxy = DBusThermometerClient(connection=connection, name='some.dbus.service', path='/path/to/test1')
        test2_proxy = DBusThermometerClient(connection=connection, name='some.dbus.service', path='/path/to/test2')

        self.assertAlmostEqual(test1_proxy.temperature(), 1)
        self.assertAlmostEqual(test2_proxy.temperature(), 2)

        service.stop()

    def test__dbus_client__in__service(self):
        '''One service contains a DBus switch object. Another service
        contains an object that accesses that former object. Challenge
        is for that object to access the existing DBus connection. '''

        lower_service = DBusService(
            daemon_address=self.daemon_address(),
            name='lower.service',
            object_creators={
                '/switch': TestSwitchObjectCreator(name='xxx', initial_state=False),
            })
        upper_service = DBusService(
            daemon_address=self.daemon_address(),
            name='upper.service',
            object_creators={
                '/switch_user_single': DBusSwitchClientObjectCreator(name='lower.service', path='/switch'),
                '/switch_user_center': SwitchCenterObjectCreator(switches={
                    'test': NativeObject(DBusSwitchClient, name='lower.service', path='/switch'),
                }),
            })

        self.__services.append(lower_service)
        self.__services.append(upper_service)

        lower_service.start()
        upper_service.start()

        self.wait_for_object(name='lower.service', path='/switch')
        self.wait_for_object(name='upper.service', path='/switch_user')

        connection = DBusClientConnection(address=self.daemon_address())

        single_proxy = DBusSwitchClient(connection=connection, name='upper.service', path='/switch_user_single')
        self.assertEqual(single_proxy.get_state(), False)

        center_proxy = DBusSwitchCenterClient(connection=connection, name='upper.service', path='/switch_user_center')
        self.assertEqual(center_proxy.get_state('test'), False)

    def test__instantiate_all_objects(self):
        # instantiate all of the different object types in a single
        # service, for the purpose of ensuring everything is
        # there. this way we can make sure no symbol errors occur late
        # at the plant.
        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={
                '/thermometers/test': TestThermometerObjectCreator(initial_temperature=1),

        '/thermometers/file': FileThermometerObjectCreator(path='/path/to/no/thermometer'),
                '/thermometers/i2c': HWMON_I2C_ThermometerObjectCreator(bus_number=666, address=0x49),
                '/thermometers/dbus': DBusThermometerClientObjectCreator(name='a.b.c', path='/some/thermometer'),
                '/switches/test': TestSwitchObjectCreator(name='testswitch', initial_state=False),
                # not easily instantiated ... '/switches/gpio': GPIOSwitchObjectCreator(gpio_number=66),
                '/switches/dbus': DBusSwitchClientObjectCreator(name='a.b.c', path='/some/switch'),
                '/switches/file': FileSwitchObjectCreator(path='/path/to/no/switch'),
                '/center/thermometers': ThermometerCenterObjectCreator(
                    thermometers={
                        'test': NativeObject(TestThermometer, initial_temperature=42),
                        'i2c': NativeObject(HWMON_I2C_Thermometer, bus_number=1, address=0x49),
                        'dbus': NativeObject(DBusThermometerClient, name='a.b.c', path='/x/y/z'),
                    }),
                '/center/switches': SwitchCenterObjectCreator(
                    switches={
                        'test': NativeObject(TestSwitch, name='testswitch', initial_state=False),
                        'dbus': NativeObject(DBusSwitchClient, name='a.b.c', path='/some/where'),
                    }),
            })

        self.__services.append(service)

        service.start()
        self.wait_for_object(name='some.dbus.service', path='/thermometers/test')

        # now talk to them
        if True:
            thermometer = DBusThermometerClient(
                connection=DBusClientConnection(address=self.daemon_address()),
                name='some.dbus.service',
                path='/thermometers/test')
            self.assertAlmostEqual(thermometer.temperature(), 1)

        if True:
            switch = DBusSwitchClient(
                connection=DBusClientConnection(address=self.daemon_address()),
                name='some.dbus.service',
                path='/switches/test')
            self.assertEqual(switch.get_state(), False)
            switch.do_close()
            self.assertEqual(switch.get_state(), True)

        if True:
            thermometer_center = DBusThermometerCenterClient(
                connection=DBusClientConnection(address=self.daemon_address()),
                name='some.dbus.service',
                path='/center/thermometers')
            self.assertAlmostEqual(thermometer_center.temperature('test'), 42)

        if True:
            switch_center = DBusSwitchCenterClient(
                connection=DBusClientConnection(address=self.daemon_address()),
                name='some.dbus.service',
                path='/center/switches')
            self.assertEqual(switch_center.get_state('test'), False)
            switch_center.set_state('test', True)
            switch_proxy = switch_center.get_switch('test')
            switch_proxy.do_close()
            self.assertEqual(switch_center.get_state('test'), True)

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
        '/path/to/switch_center': SwitchCenterObject(
            switches = {
                "switch-test-closed": TestSwitch(name='xxx', initial_state=True),
                "switch-test-open": TestSwitch(name='yyy', initial_state=False),
                # not easily instantiated ... "switch-gpio": GPIOSwitch(gpio_number=4),
                "switch-dbus": DBusSwitchClient(name="a.b.c", path="/some/path")
            }),
        '/another/path/to/thermometer_center': ThermometerCenterObject(
            thermometers = {
                "i2c-thermometer": HWMON_I2C_Thermometer(bus_number=1, address=0x49),
                "dbus-thermometer": DBusThermometerClient(name="a.b.c", path="/some/path"),
                "test-thermometer": TestThermometer(initial_temperature=4.5),
            }),
    },
    
    'some.service.thermometers': {
        '/path/to/thermometers/i2c': HWMON_I2C_ThermometerObject(bus_number=1, address=0x48),
        '/path/to/thermometers/dbus': DBusThermometerClientObject(name="a.b.c", path="/some/path"),
        '/path/to/thermometers/test': TestThermometerObject(initial_temperature=42.0),
    },

    'some.service.switches': {
        # not easily instantiated ... '/path/to/switches/gpio': GPIOSwitchObject(gpio_number=42),
        '/path/to/switches/dbus': DBusSwitchClientObject(name="a.b.c", path="/some/path"),
        '/path/to/switches/test': TestSwitchObject(name='xxx', initial_state=False),
    },
}
'''


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ServiceTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
