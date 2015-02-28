from openheating.testutils.thermometer import TestThermometer
from openheating.testutils.switch import TestSwitch

from openheating.thinking import Brain
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
        self.__brain = Brain()

        self.__source = OilWoodCombination(
            name='oil/wood',
            oil=OilCombo(
                name='source:oil', 
                thermometer=self.__oil_thermometer,
                burn_switch=self.__oil_burn_switch,
                minimum_temperature_range=Hysteresis(1,2),
                heating_range=Hysteresis(55,75),
                max_produced_temperature=90, # let's say
            ),
            wood=PassiveSource(
                name='source:wood',
                thermometer=self.__wood_thermometer,
                max_produced_temperature=50),
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

        self.__brain.add(self.__source, self.__room, self.__transport)

    def test__oil_requested_released(self):
        # room is low -> oil must come (combined forwards request to
        # oil)
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

    def test__wood_requested_released(self):
        self.fail()

    def test__wood_fades_in(self):
        self.fail()

    def test__wood_fades_out(self):
        self.fail()

    def test__wood_warm__wood_hot__overlap(self):
        # overlapping ranges of "warm" and "hot" must not be
        # possible. in fact, they should be 10 (?) apart.
        self.fail()

    def test__oil_minimum_temperature(self):
        # the "minimum temperature" logic of oil is triggered because
        # oil is-a Thinker and is registered with a Brain. I fear that
        # we could lose this when oil is part of a composition. maybe
        # we should introduce some interface method where a composite
        # Thinker would register all its delegees.
        self.fail()


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(OilWoodSourceTest))
#suite.addTest(OilWoodSourceTest('test__oil_requested_released'))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
