from openheating.dbus.switch_center_config import SwitchCenterConfig
from openheating.dbus.rebind import DBusConnectionProxy
from openheating.switch import Switch
from openheating.switch_center import SwitchCenter

import unittest

class SwitchCenterTest(unittest.TestCase):
    def test__configfile(self):
        content = '\n'.join(
            ['DAEMON_ADDRESS = "tcp:host=1.2.3.4,port=6666"',
             'BUS_NAME = "some.arbitrary.name"',

             'PATH = "/my/center"',

             'SWITCHES = (',
             '    ("switch_test_closed", TestSwitch(initial_state=CLOSED)),',
             '    ("switch_test_open", TestSwitch(initial_state=OPEN)),',
             '    ("switch_gpio", GPIOSwitch(number=4)),',
             '    ("switch_dbus", DBusSwitch(name="a.b.c", path="/some/path")),',
             ')',
             ])

        config = SwitchCenterConfig(content)

        self.assertEqual(config.daemon_address(), "tcp:host=1.2.3.4,port=6666")
        self.assertEqual(config.bus_name(), "some.arbitrary.name")

        self.assertEqual(config.path(), "/my/center")

        switch_list = list(config.iter_switches())
        
        self.assertEqual(len(switch_list), 4)

        switch_dict = dict(switch_list)

        self.assertIn('switch_test_closed', switch_dict)
        self.assertIn('switch_test_open', switch_dict)
        self.assertIn('switch_gpio', switch_dict)
        self.assertIn('switch_dbus', switch_dict)

        for name, creator in config.iter_switches():
            self.assertIsInstance(creator.create(connection_proxy=DBusConnectionProxy('')), Switch)

        center = SwitchCenter(((name, creator.create(DBusConnectionProxy(''))) for name, creator in config.iter_switches()))

        switch_test_open = center.get_switch('switch_test_open')
        self.assertTrue(switch_test_open.is_open())
        switch_test_open.do_close()
        self.assertTrue(switch_test_open.is_closed())

        switch_test_closed = center.get_switch('switch_test_closed')
        self.assertTrue(switch_test_closed.is_closed())
        switch_test_closed.do_open()
        self.assertTrue(switch_test_closed.is_open())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SwitchCenterTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
