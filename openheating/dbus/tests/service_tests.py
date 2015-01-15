from openheating.testutils.dbus_testcase import DBusTestCase
from openheating.dbus.service import DBusService
from openheating.dbus.service import TestThermometerCreator
from openheating.dbus.rebind import DBusClientConnection
from openheating.dbus.thermometer_client import DBusThermometer

import signal
import unittest


class ServiceTest(DBusTestCase):
    def setUp(self):
        super().setUp()
        self.__services = []

    def tearDown(self):
        print('ServiceTest.tearDown')
        super().tearDown()
        for s in self.__services:
            s.stop()

    def test__single_service(self):
        service = DBusService(
            daemon_address=self.daemon_address(),
            name='some.dbus.service',
            object_creators={
                '/path/to/test1': TestThermometerCreator(initial_temperature=1),
                '/path/to/test2': TestThermometerCreator(initial_temperature=2),
            })

        self.__add_service(service)

        service.start()

        self.wait_for_object(name='some.dbus.service', path='/path/to/test1')
        self.wait_for_object(name='some.dbus.service', path='/path/to/test2')

        connection = DBusClientConnection(address=self.daemon_address())
        test1_proxy = DBusThermometer(connection=connection, name='some.dbus.service', path='/path/to/test1')
        test2_proxy = DBusThermometer(connection=connection, name='some.dbus.service', path='/path/to/test2')

        self.assertAlmostEqual(test1_proxy.temperature(), 1)
        self.assertAlmostEqual(test2_proxy.temperature(), 2)

        print('stopping')
        service.stop()
        print('stopped')

    def __add_service(self, service):
        self.__services.append(service)


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ServiceTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)

# jjjj remove/rebuild this crap

# from openheating.dbus.service_config import DBusServiceConfig
# from openheating.dbus.rebind import DBusServerConnection
# from openheating.dbus.service import DBusService
# from openheating.dbus.switch_center_object import DBusSwitchCenterObject
# from openheating.dbus.thermometer_center_object import DBusThermometerCenterObject
# from openheating.dbus.switch_client import DBusSwitch
# from openheating.dbus.switch_object import DBusSwitchObject
# from openheating.dbus.thermometer_client import DBusThermometer
# from openheating.dbus.thermometer_object import DBusThermometerObject
# 
# from openheating.switch_center import SwitchCenter
# from openheating.thermometer_center import ThermometerCenter
# from openheating.testutils.switch import TestSwitch
# from openheating.testutils.thermometer import TestThermometer
# from openheating.hardware.switch_gpio import GPIOSwitch
# from openheating.hardware.thermometer_hwmon import HWMON_I2C_Thermometer
# 
# import unittest
# 
# _content = '''
# DAEMON_ADDRESS = "tcp:host=1.2.3.4,port=6666"
# 
# SERVICES = {
#     'some.service.centers': {
#         '/path/to/switch_center': SwitchCenter(
#             switches = {
#                 "switch-test-closed": TestSwitch(initial_state=CLOSED),
#                 "switch-test-open": TestSwitch(initial_state=OPEN),
#                 "switch-gpio": GPIOSwitch(number=4),
#                 "switch-dbus": DBusSwitch(name="a.b.c", path="/some/path")
#             }),
#         '/another/path/to/thermometer_center': ThermometerCenter(
#             cache_age = 5,
#             thermometers = {
#                 "i2c-thermometer": HWMON_I2C_Thermometer(bus_number=1, address=0x49),
#                 "dbus-thermometer": DBusThermometer(name="a.b.c", path="/some/path"),
#                 "test-thermometer": TestThermometer(initial_temperature=4.5),
#             }),
#     },
#     
#     'some.service.thermometers': {
#         '/path/to/thermometers/i2c': HWMON_I2C_Thermometer(bus_number=1, address=0x48),
#         '/path/to/thermometers/dbus': DBusThermometer(name="a.b.c", path="/some/path"),
#         '/path/to/thermometers/test': TestThermometer(initial_temperature=42.0),
#     },
# 
#     'some.service.switches': {
#         '/path/to/switches/gpio': GPIOSwitch(number=42),
#         '/path/to/switches/dbus': DBusSwitch(name="a.b.c", path="/some/path"),
#         '/path/to/switches/test': TestSwitch(initial_state=OPEN),
#     },
# }
# '''
#         
# class DBusServiceTest(unittest.TestCase):
#     def test__all(self):
#         config = DBusServicesConfig(_content)
# 
#         self.assertEqual(config.daemon_address(), "tcp:host=1.2.3.4,port=6666")
# 
#         services = DBusServices(creators=config.creators())
# 
#         # nothing yet happened. this is the state of the parent
#         # process, in real life, before we fork.
#         self.assertEqual(services.num_services__test(), 3)
# 
#         centers = services.get('some.service.centers')
#         thermometers = services.get('some.service.thermometers')
#         switches = services.get('some.service.switches')
# 
#         self.assertIsInstance(centers, DBusService)
#         self.assertIsInstance(thermometers, DBusService)
#         self.assertIsInstance(switches, DBusService)
# 
#         if True:
#             switch_center = centers.get('/path/to/switch_center')
#             self.assertIsInstance(switch_center, DBusObject)
#             self.assertIsInstance(switch_center, SwitchCenterObject)
#             self.assertIsInstance(switch_center.implementation(), SwitchCenter)
#             self.assertEqual(switch_center.implementation().num_switches__test(), 4)
#             self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-closed"), TestSwitch)
#             self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-open"), TestSwitch)
#             self.assertIsInstance(switch_center.implementation().get_switch__test("switch-gpio"), GPIOSwitch)
#             self.assertIsInstance(switch_center.implementation().get_switch__test("switch-dbus"), DBusSwitch)
#             self.assertTrue(switch_center.implementation().get_switch__test("switch-test-closed").is_closed())
#             self.assertTrue(switch_center.implementation().get_switch__test("switch-test-open").is_open())
# 
# 
# 
# 
# 
#         thermometer_center = centers.get('/another/path/to/thermometer_center')
# 
#         # imagine that we fork here. in the child, a DBus connection
#         # is established, everybody's enlightened with it, and DBus
#         # objects are wrapped around the local objects.
#         service.create_dbus_objects(connection=DBusServerConnection(connection=None))
# 
#         self.assertEqual(service.num_dbus_objects__test(), 8)
# 
#         switch_center = service.get_dbus_object__test("/path/to/switch_center")
#         self.assertIsNotNone(switch_center)
#         self.assertIsInstance(switch_center, DBusSwitchCenterObject)
#         self.assertIsInstance(switch_center.implementation(), SwitchCenter)
#         self.assertEqual(switch_center.implementation().num_switches__test(), 4)
#         self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-closed"), TestSwitch)
#         self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-open"), TestSwitch)
#         self.assertIsInstance(switch_center.implementation().get_switch__test("switch-gpio"), GPIOSwitch)
#         self.assertIsInstance(switch_center.implementation().get_switch__test("switch-dbus"), DBusSwitch)
#         self.assertTrue(switch_center.implementation().get_switch__test("switch-test-closed").is_closed())
#         self.assertTrue(switch_center.implementation().get_switch__test("switch-test-open").is_open())
# 
#         thermometer_center = service.get_dbus_object__test("/another/path/to/thermometer_center")
#         self.assertIsNotNone(thermometer_center)
#         self.assertIsInstance(thermometer_center, DBusThermometerCenterObject)
#         self.assertIsInstance(thermometer_center.implementation(), ThermometerCenter)
#         self.assertEqual(thermometer_center.implementation().num_thermometers__test(), 3)
#         self.assertIsInstance(thermometer_center.implementation().get_thermometer__test("i2c-thermometer"), HWMON_I2C_Thermometer)
#         self.assertIsInstance(thermometer_center.implementation().get_thermometer__test("dbus-thermometer"), DBusThermometer)
#         self.assertIsInstance(thermometer_center.implementation().get_thermometer__test("test-thermometer"), TestThermometer)
# 
#         i2c_thermometer = service.get_dbus_object__test("/path/to/thermometers/i2c")
#         self.assertIsNotNone(i2c_thermometer)
#         self.assertIsInstance(i2c_thermometer, DBusThermometerObject)
#         self.assertIsInstance(i2c_thermometer.implementation(), HWMON_I2C_Thermometer)
# 
#         dbus_thermometer = service.get_dbus_object__test("/path/to/thermometers/dbus")
#         self.assertIsNotNone(dbus_thermometer)
#         self.assertIsInstance(dbus_thermometer, DBusThermometerObject)
#         self.assertIsInstance(dbus_thermometer.implementation(), DBusThermometer)
# 
#         test_thermometer = service.get_dbus_object__test("/path/to/thermometers/test")
#         self.assertIsNotNone(test_thermometer)
#         self.assertIsInstance(test_thermometer, DBusThermometerObject)
#         self.assertIsInstance(test_thermometer.implementation(), TestThermometer)
# 
#         gpio_switch = service.get_dbus_object__test("/path/to/switches/gpio")
#         self.assertIsNotNone(gpio_switch)
#         self.assertIsInstance(gpio_switch, DBusSwitchObject)
#         self.assertIsInstance(gpio_switch.implementation(), GPIOSwitch)
# 
#         dbus_switch = service.get_dbus_object__test("/path/to/switches/dbus")
#         self.assertIsNotNone(dbus_switch)
#         self.assertIsInstance(dbus_switch, DBusSwitchObject)
#         self.assertIsInstance(dbus_switch.implementation(), DBusSwitch)
# 
#         test_switch = service.get_dbus_object__test("/path/to/switches/test")
#         self.assertIsNotNone(test_switch)
#         self.assertIsInstance(test_switch, DBusSwitchObject)
#         self.assertIsInstance(test_switch.implementation(), TestSwitch)
# 

