import unittest

class DBusObjectTest(unittest.TestCase):
    def test__all(self):
        config = DBusServicesConfig(_content)

        self.assertEqual(config.daemon_address(), "tcp:host=1.2.3.4,port=6666")

        services = DBusServices(creators=config.creators())

        # nothing yet happened. this is the state of the parent
        # process, in real life, before we fork.
        self.assertEqual(services.num_services__test(), 3)

        centers = services.get('some.service.centers')
        thermometers = services.get('some.service.thermometers')
        switches = services.get('some.service.switches')

        self.assertIsInstance(centers, DBusService)
        self.assertIsInstance(thermometers, DBusService)
        self.assertIsInstance(switches, DBusService)

        if True:
            switch_center = centers.get('/path/to/switch_center')
            self.assertIsInstance(switch_center, DBusObject)
            self.assertIsInstance(switch_center, SwitchCenterObject)
            self.assertIsInstance(switch_center.implementation(), SwitchCenter)
            self.assertEqual(switch_center.implementation().num_switches__test(), 4)
            self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-closed"), TestSwitch)
            self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-open"), TestSwitch)
            self.assertIsInstance(switch_center.implementation().get_switch__test("switch-gpio"), GPIOSwitch)
            self.assertIsInstance(switch_center.implementation().get_switch__test("switch-dbus"), DBusSwitch)
            self.assertTrue(switch_center.implementation().get_switch__test("switch-test-closed").is_closed())
            self.assertTrue(switch_center.implementation().get_switch__test("switch-test-open").is_open())





        thermometer_center = centers.get('/another/path/to/thermometer_center')

        # imagine that we fork here. in the child, a DBus connection
        # is established, everybody's enlightened with it, and DBus
        # objects are wrapped around the local objects.
        service.create_dbus_objects(connection=DBusServerConnection(connection=None))

        self.assertEqual(service.num_dbus_objects__test(), 8)

        switch_center = service.get_dbus_object__test("/path/to/switch_center")
        self.assertIsNotNone(switch_center)
        self.assertIsInstance(switch_center, DBusSwitchCenterObject)
        self.assertIsInstance(switch_center.implementation(), SwitchCenter)
        self.assertEqual(switch_center.implementation().num_switches__test(), 4)
        self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-closed"), TestSwitch)
        self.assertIsInstance(switch_center.implementation().get_switch__test("switch-test-open"), TestSwitch)
        self.assertIsInstance(switch_center.implementation().get_switch__test("switch-gpio"), GPIOSwitch)
        self.assertIsInstance(switch_center.implementation().get_switch__test("switch-dbus"), DBusSwitch)
        self.assertTrue(switch_center.implementation().get_switch__test("switch-test-closed").is_closed())
        self.assertTrue(switch_center.implementation().get_switch__test("switch-test-open").is_open())

        thermometer_center = service.get_dbus_object__test("/another/path/to/thermometer_center")
        self.assertIsNotNone(thermometer_center)
        self.assertIsInstance(thermometer_center, DBusThermometerCenterObject)
        self.assertIsInstance(thermometer_center.implementation(), ThermometerCenter)
        self.assertEqual(thermometer_center.implementation().num_thermometers__test(), 3)
        self.assertIsInstance(thermometer_center.implementation().get_thermometer__test("i2c-thermometer"), HWMON_I2C_Thermometer)
        self.assertIsInstance(thermometer_center.implementation().get_thermometer__test("dbus-thermometer"), DBusThermometer)
        self.assertIsInstance(thermometer_center.implementation().get_thermometer__test("test-thermometer"), TestThermometer)

        i2c_thermometer = service.get_dbus_object__test("/path/to/thermometers/i2c")
        self.assertIsNotNone(i2c_thermometer)
        self.assertIsInstance(i2c_thermometer, DBusThermometerObject)
        self.assertIsInstance(i2c_thermometer.implementation(), HWMON_I2C_Thermometer)

        dbus_thermometer = service.get_dbus_object__test("/path/to/thermometers/dbus")
        self.assertIsNotNone(dbus_thermometer)
        self.assertIsInstance(dbus_thermometer, DBusThermometerObject)
        self.assertIsInstance(dbus_thermometer.implementation(), DBusThermometer)

        test_thermometer = service.get_dbus_object__test("/path/to/thermometers/test")
        self.assertIsNotNone(test_thermometer)
        self.assertIsInstance(test_thermometer, DBusThermometerObject)
        self.assertIsInstance(test_thermometer.implementation(), TestThermometer)

        gpio_switch = service.get_dbus_object__test("/path/to/switches/gpio")
        self.assertIsNotNone(gpio_switch)
        self.assertIsInstance(gpio_switch, DBusSwitchObject)
        self.assertIsInstance(gpio_switch.implementation(), GPIOSwitch)

        dbus_switch = service.get_dbus_object__test("/path/to/switches/dbus")
        self.assertIsNotNone(dbus_switch)
        self.assertIsInstance(dbus_switch, DBusSwitchObject)
        self.assertIsInstance(dbus_switch.implementation(), DBusSwitch)

        test_switch = service.get_dbus_object__test("/path/to/switches/test")
        self.assertIsNotNone(test_switch)
        self.assertIsInstance(test_switch, DBusSwitchObject)
        self.assertIsInstance(test_switch.implementation(), TestSwitch)

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DBusServiceTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
