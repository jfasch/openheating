from openheating.testutils.plant_testcase import PlantTestCase
from openheating.testutils import testutils
from openheating.plant.simple_plant import SimplePlant

import unittest
import time
import itertools


class CircuitsTest(PlantTestCase):
    def setUp(self):
        super().setUp()

        self.__plant = SimplePlant(bus=self.bus, make_tempfile=self.tempfile, make_tempdir=self.tempdir)
        self.start_plant(self.__plant)
        self.__clients = self.__plant.create_clients()

        # timestamps for injected samples
        self.__timeline = itertools.count()

        # provide initial values
        self.__plant.producer_file_thermometer.set_temperature(10)
        self.__plant.consumer_file_thermometer.set_temperature(10)
        self.__plant.pump_file_switch.set_state(False)

        self.force_temperature_update(next(self.__timeline))

    @PlantTestCase.intercept_failure
    def test__activate_deactivate(self):
        self.__clients.circuit.activate()
        self.assertTrue(self.__clients.circuit.is_active())

        self.__clients.circuit.deactivate()
        self.assertFalse(self.__clients.circuit.is_active())

    @PlantTestCase.intercept_failure
    def test__pump_on_off(self):
        # paranoia. we injected samples to give 10 degrees.
        self.assertAlmostEqual(self.__clients.consumer_thermometer.get_temperature(), 10)
        self.assertAlmostEqual(self.__clients.producer_thermometer.get_temperature(), 10)

        self.__clients.circuit.activate()
        self.__clients.circuit.poll(0) # epoch
        self.assertFalse(self.__clients.pump_switch.get_state())

        # produce heat
        self.__plant.producer_file_thermometer.set_temperature(50)
        self.force_temperature_update(timestamp=next(self.__timeline))
        # paranoia
        self.assertAlmostEqual(self.__clients.producer_thermometer.get_temperature(), 50)

        self.__clients.circuit.poll(next(self.__timeline))
        self.assertTrue(self.__clients.pump_switch.get_state())

        # consume heat, but do not yet trigger hysteresis.
        self.__plant.consumer_file_thermometer.set_temperature(45)
        self.force_temperature_update(timestamp=next(self.__timeline))
        # paranoia
        self.assertAlmostEqual(self.__clients.consumer_thermometer.get_temperature(), 45)

        # pump still on (hysteresis lower bound is 3)
        self.__clients.circuit.poll(next(self.__timeline))
        self.assertTrue(self.__clients.pump_switch.get_state())
        
        # consume even more heat; difference goes below 3
        self.__plant.consumer_file_thermometer.set_temperature(48)
        self.force_temperature_update(timestamp=next(self.__timeline))
        # paranoia
        self.assertAlmostEqual(self.__clients.consumer_thermometer.get_temperature(), 48)

        # pump off
        self.__clients.circuit.poll(next(self.__timeline))
        self.assertFalse(self.__clients.pump_switch.get_state())
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CircuitsTest))

if __name__ == '__main__':
    testutils.run(suite)

