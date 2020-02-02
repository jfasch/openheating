from openheating.base.switch import FileSwitch
from openheating.dbus.switch_center import SwitchCenter_Client
from openheating.plant import service
from openheating.plant.plant import Plant
from openheating.testutils import testutils
from openheating.testutils.plant_testcase import PlantTestCase

import unittest
import os.path


class SwitchesTest(PlantTestCase):
    def setUp(self):
        super().setUp()
        self.__tmpdir = self.tempdir()

    def test__basic(self):
        config=self.tempfile(
            lines=[
                'from openheating.base.switch import InMemorySwitch',
                'ADD_SWITCH("TestSwitch", "Test Switch", InMemorySwitch(False))',
            ]
        )
        self.start_plant(Plant([service.SwitchService(config=config.name)]))

        center_client = SwitchCenter_Client(self.bus)
        switch_client = center_client.get_switch('TestSwitch')
        self.assertEqual(switch_client.get_name(), 'TestSwitch')
        self.assertEqual(switch_client.get_description(), 'Test Switch')
        self.assertEqual(switch_client.get_state(), False)
        switch_client.set_state(True)
        self.assertEqual(switch_client.get_state(), True)

    def test__simulation_dir__passed(self):
        swdir = self.__tmpdir.name+'/some/dir/to/contain/switches'
        config=self.tempfile(
            lines=[
                'from openheating.base.switch import InMemorySwitch',
                'assert IS_SIMULATION',
                'ADD_SWITCH("TestSwitch", "Test Switch", None)',
            ]
        )

        self.start_plant(Plant([ 
            service.SwitchService(
                config=config.name,
                simulation_dir=swdir,
            )]))
        
        self.assertTrue(os.path.isdir(swdir)) # created by service process
        self.assertTrue(os.path.isfile(swdir+'/TestSwitch'))

        # read initial switch state (thereby verifying that the file
        # has been created by the service, and initialized with
        # False). (use PlantTestCase convenience methods for all
        # this.)
        self.assertFalse(self.get_switchstate_file('TestSwitch'))

        # set switch via dbus; verify file state
        self.set_switchstate_dbus('TestSwitch', True)
        self.assertTrue(self.get_switchstate_file('TestSwitch'))

        # set switch via file (an input switch so to say), and verify
        # via dbus
        self.set_switchstate_file('TestSwitch', False)
        self.assertFalse(self.get_switchstate_dbus('TestSwitch'))

        self.set_switchstate_file('TestSwitch', True)
        self.assertTrue(self.get_switchstate_dbus('TestSwitch'))

    def test__simulation_dir__not_passed(self):
        switch_file = self.tempfile(suffix='.switch')
        config=self.tempfile(
            lines=[
                'from openheating.base.switch import FileSwitch',

                'assert not IS_SIMULATION',

                # simulation is off. we expect the switch to be
                # added as-is.
                'ADD_SWITCH(',
                '      "test_name", "test description",',
                '      FileSwitch("{}", initial_value=True))'.format(switch_file.name),
            ],
            suffix='.switches-config',
        )
        self.start_plant(Plant([service.SwitchService(config=config.name)]))
 
        # simulation is off, so the switch must have been taken as-is
        # => file contains the initial value as specified by config.
        self.assertTrue(FileSwitch(switch_file.name).get_state(), True)
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SwitchesTest))

if __name__ == '__main__':
    testutils.run(suite)

