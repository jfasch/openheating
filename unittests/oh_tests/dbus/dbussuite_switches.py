from openheating.dbus.switch_center import SwitchCenter_Client

from openheating.test import service
from openheating.test import testutils
from openheating.test.plant_testcase import PlantTestCase
from openheating.test.plant import Plant

import pydbus

import unittest
import os.path


class SwitchesTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__tmpdir = self.tempdir()

    def test__basic(self):
        config=self.tempfile(
            lines=[
                'from openheating.base.switch import DummySwitch',
                'ADD_SWITCH(DummySwitch("TestSwitch", "Test Switch", False))',

                'assert GET_SIMULATED_SWITCHES_DIR() is None, GET_SIMULATED_SWITCHES_DIR()',
            ]
        )
        self.start_plant(Plant([service.SwitchService(config=config.name)]))

        center_client = SwitchCenter_Client(pydbus.SessionBus())
        switch_client = center_client.get_switch('TestSwitch')
        self.assertEqual(switch_client.get_name(), 'TestSwitch')
        self.assertEqual(switch_client.get_description(), 'Test Switch')
        self.assertEqual(switch_client.get_state(), False)
        switch_client.set_state(True)
        self.assertEqual(switch_client.get_state(), True)

    def test__simulated_dir(self):
        swdir = self.__tmpdir.name+'/some/dir/to/contain/switches'
        config=self.tempfile(
            lines=[
                'from openheating.base.switch import DummySwitch',
                'ADD_SWITCH(DummySwitch("TestSwitch", "Test Switch", False))',

                'assert GET_SIMULATED_SWITCHES_DIR() == "{}", GET_SIMULATED_SWITCHES_DIR()'.format(swdir),
            ]
        )

        self.start_plant(Plant([
            service.SwitchService(
                config=config.name,
                simulated_switches_dir=swdir,
            ),
        ]))
        
        self.assertTrue(os.path.isdir(swdir)) # created by service process

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SwitchesTest))

if __name__ == '__main__':
    testutils.run(suite)

