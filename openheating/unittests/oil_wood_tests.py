from openheating.testutils.thermometer import TestThermometer
from openheating.testutils.switch import TestSwitch

from openheating.brain import Brain
from openheating.sink import Sink
from openheating.transport import Transport
from openheating.hysteresis import Hysteresis
from openheating.oil import OilCombo
from openheating.passive_source import PassiveSource
from openheating.oil_wood import OilWoodCombination

import logging
import unittest


class OilWoodSourceTest(unittest.TestCase):
    def setUp(self):
        self.__brain = Brain()

        self.__oil_thermometer = TestThermometer(initial_temperature=15)
        self.__wood_thermometer = TestThermometer(initial_temperature=20)
        self.__room_thermometer = TestThermometer(initial_temperature=20)
        self.__oil_burn_switch = TestSwitch(name='switch:oil-burn', initial_state=False)
        self.__pump_switch = TestSwitch(name='switch:pump', initial_state=False)
        self.__valve_switch = TestSwitch(name='switch:valve', initial_state=False)

        self.__oil = OilCombo(
            name='source:oil', 
            thermometer=self.__oil_thermometer,
            burn_switch=self.__oil_burn_switch,
            minimum_temperature_range=Hysteresis(5,6),
            heating_range=Hysteresis(50,60),
            max_produced_temperature=90, # let's say
        )
        self.__wood = PassiveSource(
            name='source:wood',
            thermometer=self.__wood_thermometer,
            max_produced_temperature=50)

        self.__brain = Brain()

        self.__source = OilWoodCombination(
            name='oil/wood',
            oil=self.__oil,
            wood=self.__wood,
            valve_switch=self.__valve_switch,
            wood_warm=Hysteresis(30, 32),
            wood_hot=Hysteresis(40, 42),
        )

        self.__room = Sink(
            name='sink',
            thermometer=self.__room_thermometer,
            temperature_range=Hysteresis(21, 23))

        self.__transport = Transport(
            name='transport',
            source=self.__source, 
            sink=self.__room,
            diff_hysteresis=Hysteresis(2,5),
            pump_switch=self.__pump_switch)

        self.__source.register_thinking(self.__brain)
        self.__room.register_thinking(self.__brain)
        self.__transport.register_thinking(self.__brain)

    def test__oil_requested_released(self):
        'the most simple case. wood remains cold, all requests to oil'

        # room is low -> oil must come (combined-source forwards
        # request to oil)
        self.__brain.think('initially, oil is on')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertTrue(self.__oil_burn_switch.is_closed())
        self.assertEqual(self.__source.num_requests(), 1)

        # room inside range -> oil still burning
        self.__room_thermometer.set_temperature(22)
        self.__brain.think('room goes at 22 (inside range), oil still there')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertTrue(self.__oil_burn_switch.is_closed())
        self.assertEqual(self.__source.num_requests(), 1)

        # room satisfied -> oil off
        self.__room_thermometer.set_temperature(24)
        self.__brain.think('room at 24, enough, oil off')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertTrue(self.__oil_burn_switch.is_open())
        self.assertEqual(self.__source.num_requests(), 0)

    def test__wood_comes(self):
        '''wood comes; passes through all stages oil, fade in, wood'''

        # initially, everything's on oil
        self.__brain.think('initial, there\'s oil')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertTrue(self.__oil_burn_switch.is_closed())
        # one request (oil)
        self.assertEqual(self.__source.num_requests(), 1)
        self.assertEqual(self.__oil.num_requests(), 1)
        self.assertEqual(self.__wood.num_requests(), 0)

        # let wood come. lower bound of "wood is warm" is 30, so heat
        # wood up to this point. no change, it's the lower
        # end. requests still directed towards oil, valve at oil.
        self.__wood_thermometer.set_temperature(30.1)
        self.__brain.think('wood becomes warm, but still only at lower end')
        # one request (oil)
        self.assertEqual(self.__source.num_requests(), 1)
        self.assertEqual(self.__oil.num_requests(), 1)
        self.assertEqual(self.__wood.num_requests(), 0)
        self.assertTrue(self.__valve_switch.is_open())

        # wood's temperature rises above "warm" hysteresis (32 being
        # its upper end). state change; requests go to wood. oil stops
        # burning, valve still at oil (oil fades out slowly).
        self.__wood_thermometer.set_temperature(32.1)
        self.__brain.think('wood definitely becomes warm, threshold reached')
        # one request (wood)
        self.assertEqual(self.__source.num_requests(), 1)
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__valve_switch.is_open())

        # wood rises at between "wood hot" hysteresis (whose lower end
        # is 40). no change because we are only at lower end.
        self.__wood_thermometer.set_temperature(40.1)
        self.__brain.think('wood almost hot now, but not yet through threshold')
        # one request (wood)
        self.assertEqual(self.__source.num_requests(), 1)
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__valve_switch.is_open())
        
        # wood rises at above "wood hot" hysteresis (whose upper end
        # is 42).
        self.__wood_thermometer.set_temperature(42.1)
        self.__brain.think('wood hot')
        # one request (wood)
        self.assertEqual(self.__source.num_requests(), 1)
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__valve_switch.is_closed())

    def test__wood_fades_in__oil_hot(self):
        self.__oil_thermometer.set_temperature(70)
        self.__wood_thermometer.set_temperature(20)

        self.__brain.think('wood cold, oil hot')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 1)
        self.assertEqual(self.__wood.num_requests(), 0)
        self.assertTrue(self.__pump_switch.is_closed())

        # wood warms up. oil not requested, but wood is. valve still
        # at oil, pump on. requests are already directed to wood,
        # valve position already at oil.
        self.__wood_thermometer.set_temperature(32.1) # right above "warm" hyst.
        self.__brain.think('wood warm, oil still hot')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__pump_switch.is_closed())

        # wood between "hot" hysteresis. not yet considered hot,
        # situation as above.
        self.__wood_thermometer.set_temperature(41) # right above "warm" hyst.
        self.__brain.think('wood almost hot, oil still hot')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__pump_switch.is_closed())

        # wood hot. requests *and* valve position go
        # there. *regardless* of oil's temperature.
        self.__wood_thermometer.set_temperature(45) # right above "warm" hyst.
        self.__brain.think('wood hot, oil still hot')
        self.assertTrue(self.__valve_switch.is_closed())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__pump_switch.is_closed())

    def test__wood_fades_out(self):
        self.__oil_thermometer.set_temperature(70)
        self.__wood_thermometer.set_temperature(50)

        self.__brain.think('wood hot, oil hot')
        self.assertTrue(self.__valve_switch.is_closed())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__pump_switch.is_closed())

        # wood cools down, under "hot" hysteresis. oil is hotter than
        # wood, so valve is switched there. requests go still to wood,
        # as this is maybe only temporary.
        self.__wood_thermometer.set_temperature(39)
        self.__brain.think('wood right below hot, oil hot')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__pump_switch.is_closed())

        # wood still cools down. lets say for a moment that oil is
        # cooler than wood - in this case the valve has to wood.
        self.__oil_thermometer.set_temperature(38)
        self.__brain.think('wood right below hot, oil cool')
        self.assertTrue(self.__valve_switch.is_closed())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__pump_switch.is_closed())

        # (revert the above situation, it is just a test that we do in
        # between)
        self.__oil_thermometer.set_temperature(38)

        # wood between "warm" hysteresis. situation as above.
        self.__wood_thermometer.set_temperature(31)
        self.__brain.think('wood almost cold, oil hot')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 1)
        self.assertTrue(self.__pump_switch.is_closed())

        # wood cold. requests go to oil.
        self.__wood_thermometer.set_temperature(25)
        self.__brain.think('wood almost cold, oil hot')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 1)
        self.assertEqual(self.__wood.num_requests(), 0)
        self.assertTrue(self.__pump_switch.is_closed())

    def test__wood_warm__wood_hot__overlap(self):
        # overlapping ranges of "warm" and "hot" must not be
        # possible. in fact, they should be 10 (?) apart.
        try:
            OilWoodCombination(
                name='oil/wood',
                oil=self.__oil,
                wood=self.__wood,
                valve_switch=self.__valve_switch,
                wood_warm=Hysteresis(30, 32),
                wood_hot=Hysteresis(31, 33),
            )
            self.fail()
        except AssertionError:
            pass

    def test__oil_minimum_temperature(self):
        '''the "minimum temperature" logic of oil is triggered because oil
        is-a Thinker and is registered with a Brain. I fear that we
        could lose this when oil is part of a composition.

        '''

        # all off initially, room satisfied, everything quiet.
        self.__room_thermometer.set_temperature(25)
        self.__oil_thermometer.set_temperature(20)
        self.__wood_thermometer.set_temperature(20)
        self.__brain.think('all cool, all off')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 0)
        self.assertTrue(self.__pump_switch.is_open())

        # oil cools to a point where it's really cold -> anti-freeze
        # program, for the purpose of saving the life of the oil
        # plant.
        self.__oil_thermometer.set_temperature(1)
        self.__brain.think('oil anti-freeze')
        self.assertTrue(self.__valve_switch.is_open())
        self.assertEqual(self.__oil.num_requests(), 0)
        self.assertEqual(self.__wood.num_requests(), 0)
        self.assertTrue(self.__pump_switch.is_open())
        # here we go: oil burns
        self.__oil_burn_switch.is_closed()


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(OilWoodSourceTest))
#suite.addTest(OilWoodSourceTest('test__oil_minimum_temperature'))
#print('jjjjjjjjjjjjjjjjjjj')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
