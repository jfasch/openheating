from openheating.dbus.switch_center import SwitchCenter_Client

from openheating.test import service
from openheating.test import testutils
from openheating.test.plant_testcase import PlantTestCase
from openheating.test.plant import Plant

import pydbus

import unittest


class SwitchesTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.start_plant(Plant([
            service.SwitchService(pyconf=[
                'from openheating.base.switch import DummySwitch',
                'SWITCHES = [',
                '    DummySwitch("TestSwitch", "Test Switch", False),',
                ']'
            ]),
        ]))

    def test__basic(self):
        center_client = SwitchCenter_Client(pydbus.SessionBus())
        switch_client = center_client.get_switch('TestSwitch')
        self.assertEqual(switch_client.get_name(), 'TestSwitch')
        self.assertEqual(switch_client.get_description(), 'Test Switch')
        self.assertEqual(switch_client.get_state(), False)
        switch_client.set_state(True)
        self.assertEqual(switch_client.get_state(), True)


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SwitchesTest))

if __name__ == '__main__':
    testutils.run(suite)

