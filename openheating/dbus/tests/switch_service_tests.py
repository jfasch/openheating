from openheating.testutils.switch import TestSwitch
from openheating.hardware.switch_gpio import GPIOSwitch
from openheating.dbus.switch_service_config import SwitchServiceConfig

import unittest

class SwitchServiceTest(unittest.TestCase):
    def test__configfile(self):
        content = '\n'.join(
            ['DAEMON_ADDRESS = "tcp:host=1.2.3.4,port=6666"',
             'BUS_NAME = "some.arbitrary.name"',
             'PARENT_PATH = "/my/switches"',

             'SWITCHES = (',
             '    ("switch_gpio", GPIOSwitch(number=4)),',
             '    ("switch_test_open", TestSwitch(initial_state=OPEN)),',
             '    ("switch_test_closed", TestSwitch(initial_state=CLOSED)),',
             ')',
             ])
        
        config = SwitchServiceConfig(content)

        self.failUnlessEqual(config.daemon_address(), "tcp:host=1.2.3.4,port=6666")
        self.failUnlessEqual(config.bus_name(), "some.arbitrary.name")

        self.failUnlessEqual(config.switches()[0]['object_path'], '/my/switches/switch_gpio')
        self.failUnless(isinstance(config.switches()[0]['switch'], GPIOSwitch))

        self.failUnlessEqual(config.switches()[1]['object_path'], '/my/switches/switch_test_open')
        self.failUnless(isinstance(config.switches()[1]['switch'], TestSwitch))

        self.failUnlessEqual(config.switches()[2]['object_path'], '/my/switches/switch_test_closed')
        self.failUnless(isinstance(config.switches()[2]['switch'], TestSwitch))

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SwitchServiceTest))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
