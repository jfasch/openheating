from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils
from openheating.plant import simple_plant

import unittest
import time
import itertools


class CircuitsTest(PlantTestCase):
    def setUp(self):
        super().setUp()

        self.start_plant(simple_plant.create_without_main(
            make_tempfile=self.tempfile,
            make_tempdir=self.tempdir))

        # timestamps for injected samples
        self.__timeline = itertools.count()

        # provide initial values
        self.set_temperature_files_and_update({'producer': 10, 'consumer': 10},
                                              timestamp=next(self.__timeline))
        self.set_switchstate_file('pump', False)

    @PlantTestCase.intercept_failure
    def test__activate_deactivate(self):
        self.activate_circuit('TestCircuit')
        self.assertTrue(self.is_circuit_active('TestCircuit'))

        self.deactivate_circuit('TestCircuit')
        self.assertFalse(self.is_circuit_active('TestCircuit'))

    @PlantTestCase.intercept_failure
    def test__pump_on_off(self):
        # paranoia. we initialized thermometers to give 10 degrees.
        self.assertAlmostEqual(self.get_temperature_dbus('consumer'), 10)
        self.assertAlmostEqual(self.get_temperature_dbus('producer'), 10)

        self.activate_circuit('TestCircuit')
        self.poll_circuit('TestCircuit', timestamp=0) # epoch
        self.assertFalse(self.get_switchstate_file('pump'))

        # produce heat
        self.set_temperature_file_and_update('producer', 50, timestamp=next(self.__timeline))
        # paranoia (testing test-code)
        self.assertAlmostEqual(self.get_temperature_dbus('producer'), 50)

        self.poll_circuit('TestCircuit', timestamp=next(self.__timeline))
        self.assertTrue(self.get_switchstate_file('pump'))

        # consume heat, but do not yet trigger hysteresis.
        self.set_temperature_file_and_update('consumer', 45, timestamp=next(self.__timeline))
        # paranoia (testing test-code)
        self.assertAlmostEqual(self.get_temperature_dbus('consumer'), 45)

        # pump still on (hysteresis lower bound is 3)
        self.poll_circuit('TestCircuit', timestamp=next(self.__timeline))
        self.assertTrue(self.get_switchstate_file('pump'))
        
        # consume even more heat; difference goes below 3
        self.set_temperature_file_and_update('consumer', 48, timestamp=next(self.__timeline))
        # paranoia (testing test-code)
        self.assertAlmostEqual(self.get_temperature_dbus('consumer'), 48)

        # pump off
        self.poll_circuit('TestCircuit', timestamp=next(self.__timeline))
        self.assertFalse(self.get_switchstate_file('pump'))

    def test__pump_off_when_deactivated(self):
        # paranoia
        self.assertFalse(self.is_circuit_active('TestCircuit'))
        self.assertFalse(self.get_switchstate_file('pump'))

        self.activate_circuit('TestCircuit')
        self.assertFalse(self.get_switchstate_file('pump'))
        self.set_temperature_file_and_update('producer', 30, timestamp=next(self.__timeline))

        self.poll_circuit('TestCircuit', timestamp=next(self.__timeline))
        self.assertTrue(self.get_switchstate_file('pump'))

        self.deactivate_circuit('TestCircuit')
        self.assertFalse(self.get_switchstate_file('pump'))

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CircuitsTest))

if __name__ == '__main__':
    testutils.run(suite)

