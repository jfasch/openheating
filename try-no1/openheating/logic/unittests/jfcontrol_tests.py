from openheating.testutils.test_thermometer import TestThermometer
from openheating.testutils.test_switch import TestSwitch

from openheating.logic.jf_control import JFControl
from openheating.logic.brain import Brain
from openheating.logic.switch_center import SwitchCenter, SwitchCenterSwitch
from openheating.logic.thermometer_center import ThermometerCenter, ThermometerCenterThermometer

import unittest
import logging
import pprint


class JFControlTest(unittest.TestCase):
    def setUp(self):
        # setup temperatures so that everyone's satisfied, nothing is
        # going on.
        self.__th_room = TestThermometer(initial_temperature=23)
        self.__th_water = TestThermometer(initial_temperature=60)
        self.__th_wood = TestThermometer(initial_temperature=23)
        self.__th_oil = TestThermometer(initial_temperature=23)

        self.__sw_water = TestSwitch('water', initial_state=False)
        self.__sw_room = TestSwitch('room', initial_state=False)
        self.__sw_oil = TestSwitch('oil', initial_state=False)
        self.__sw_wood_valve = TestSwitch('valve', initial_state=False)

        self.__jfcontrol = JFControl(
            switch_center = SwitchCenter({
                'water': self.__sw_water,
                'room': self.__sw_room,
                'oil': self.__sw_oil,
                'valve': self.__sw_wood_valve,
            }),
            thermometer_center = ThermometerCenter({
                'room': self.__th_room,
                'water': self.__th_water,
                'wood': self.__th_wood,
                'oil': self.__th_oil,
            }),
            th_room = 'room',
            th_water = 'water',
            th_wood = 'wood',
            th_oil = 'oil',
            sw_water = 'water',
            sw_room = 'room',
            sw_oil = 'oil',
            sw_wood_valve = 'valve')

        self.__brain = Brain([self.__jfcontrol])

    def test__all_silent_initially(self):
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

    def test__scenario__demo__oilonly__stepback(self):
        '''demo scenario: oil only; show how consumers step back in favor of each other'''

        # water falls to 20 which is far too cold. oil starts burning.
        self.__th_water.set_temperature(20)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), True)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # oil heats up to 40. oil still burning. additionally, the
        # warm-water pump switches on.
        self.__th_oil.set_temperature(40)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), True)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), True)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # oil heats up to 70 (which is right below its max). oil still
        # burning, pump still pumping.
        self.__th_oil.set_temperature(70)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), True)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), True)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # oil heats up to 71 (reached its max). oil off, pump still
        # on.
        self.__th_oil.set_temperature(71)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), True)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # now the warm water is satisfied - 56. oil is still at 71
        # though. now we are two sinks that don't need (room is still
        # at 23 and satisfied), so *everybody* gets its
        # share. room-pump switches on in addition.
        self.__th_water.set_temperature(56)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), True)
        self.assertEqual(self.__sw_room.get_state(), True)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # STEP-BACK: room falls to 15 - not satisfied anymore. water
        # steps back in favor of room (room *does* need, water
        # *doesn't*).
        self.__th_room.set_temperature(15)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), True)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # room rises again, to 23. satisfied. *both* satisfied ->
        # *both* pumps running.
        self.__th_room.set_temperature(23)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), True)
        self.assertEqual(self.__sw_room.get_state(), True)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # oil falls to 25. room still at 23, water at 56. both
        # satisfied, but there's still difference between oil and
        # room.
        self.__th_oil.set_temperature(25)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), True)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # oil falls to 23. all silent again.
        self.__th_oil.set_temperature(23)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

    def test__scenario__demo__switching_between_oil_and_wood(self):
        '''demo scenario: wood coming while oil is warm, then hot enough and switching over. '''

        # oil is at 40, initially. everyone's satisfied. water is at
        # 60, so it cannot take 40. but room is at 23, and it will
        # take.
        self.__th_oil.set_temperature(40)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), True)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # wood heats up at 33 (this is the temperature where we know
        # that wood is coming). oil is still at 40, and room still
        # takes from there.
        self.__th_wood.set_temperature(33)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), True)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # oil cools down to 21. all idle again, wood still only coming
        # and not active - hence room is off.
        self.__th_oil.set_temperature(21)
        self.__brain.think()

        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)

        # water falls to 20. there's *definitely* a need (water's
        # low-threshold is 50). wood is not hot enough to be
        # activated. BUT: we know wood is coming, so oil *won't* burn
        # as would be the case otherwise.
        self.__th_water.set_temperature(20)
        self.__brain.think()
        
        self.assertEqual(self.__sw_water.get_state(), False)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), False)
        
        # wood heats up to 43 which is "hot". activate wood. water
        # will take. room - which is satisfied - steps back in favor
        # of water.
        self.__th_wood.set_temperature(43)
        pprint.pprint(self.__brain.think())

        self.assertEqual(self.__sw_water.get_state(), True)
        self.assertEqual(self.__sw_room.get_state(), False)
        self.assertEqual(self.__sw_oil.get_state(), False)
        self.assertEqual(self.__sw_wood_valve.get_state(), True)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(JFControlTest)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
