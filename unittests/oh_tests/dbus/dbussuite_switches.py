from openheating.dbus.switch_center import SwitchCenter_Client

from openheating.test import service
from openheating.test import testutils
from openheating.test.plant_testcase import PlantTestCase
from openheating.test.plant import Plant

import pydbus

import unittest
import os.path


class SwitchesTest(PlantTestCase):
    def test__basic(self):
        self.start_plant(Plant([
            service.SwitchService(
                config=[
                    'from openheating.base.switch import DummySwitch',
                    'ADD_SWITCH(DummySwitch("TestSwitch", "Test Switch", False))',

                    'assert GET_SIMULATED_SWITCHES_DIR() is None, GET_SIMULATED_SWITCHES_DIR()',
                ]),
        ]))

        center_client = SwitchCenter_Client(pydbus.SessionBus())
        switch_client = center_client.get_switch('TestSwitch')
        self.assertEqual(switch_client.get_name(), 'TestSwitch')
        self.assertEqual(switch_client.get_description(), 'Test Switch')
        self.assertEqual(switch_client.get_state(), False)
        switch_client.set_state(True)
        self.assertEqual(switch_client.get_state(), True)

    def test__simulated_dir(self):
        self.start_plant(Plant([
            service.SwitchService(
                config=[
                    'from openheating.base.switch import DummySwitch',
                    'ADD_SWITCH(DummySwitch("TestSwitch", "Test Switch", False))',

                    'assert GET_SIMULATED_SWITCHES_DIR() == "/tmp/some/dir/to/contain/switches", GET_SIMULATED_SWITCHES_DIR()',
                ],
                simulated_switches_dir='/tmp/some/dir/to/contain/switches',
            ),
        ]))
        
        self.assertTrue(os.path.isdir('/tmp/some/dir/to/contain/switches'))

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SwitchesTest))

if __name__ == '__main__':
    testutils.run(suite)

