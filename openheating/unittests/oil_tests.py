from openheating.testutils.thermometer import TestThermometer
from openheating.testutils.switch import TestSwitch

from openheating.thinking import Brain
from openheating.sink import Sink
from openheating.transport import Transport
from openheating.hysteresis import Hysteresis
from openheating.oil import OilCombo

import unittest
import logging


class OilComboTest(unittest.TestCase):
    def setUp(self):
        self.__brain = Brain()
        
        self.__sink_thermometer = TestThermometer(initial_temperature=20)
        self.__sink = Sink(name='my-sink', thermometer=self.__sink_thermometer, temperature_range=Hysteresis(low=40, high=45))
        self.__sink.register_thinking(self.__brain)

        self.__oil_thermometer = TestThermometer(initial_temperature=20)
        self.__oil_burn_switch = TestSwitch(name='oil-burn', initial_state=False)

        self.__oil_combo = OilCombo(
            name='my-oil-combo', 
            thermometer=self.__oil_thermometer,
            burn_switch=self.__oil_burn_switch,
            minimum_temperature_range=Hysteresis(1,2),
            heating_range=Hysteresis(55,75),
            max_produced_temperature=90, # let's say
        )

        self.__transport = Transport(name='my-transport',
                                     source=self.__oil_combo, sink=self.__sink,
                                     diff_hysteresis=Hysteresis(0, 5),
                                     pump_switch=TestSwitch(name='pump', initial_state=False))
        self.__transport.register_thinking(self.__brain)
        self.__oil_combo.register_thinking(self.__brain)

    def test__request_release(self):
        '''Play the standard source/sink game'''

        self.assertTrue(self.__oil_burn_switch.is_open())

        # sink is way below wanted, so after thinking oil must be
        # requested
        self.__brain.think('sink way below wanted')
        if True:
            self.assertTrue(self.__oil_combo.is_requested_by(self.__sink))
            self.assertTrue(self.__oil_burn_switch.is_closed())

        # sink temperature rises above wanted -> release
        self.__sink_thermometer.set_temperature(50)
        self.__brain.think('sink above wanted')
        if True:
            self.assertFalse(self.__oil_combo.is_requested_by(self.__sink))
            self.assertTrue(self.__oil_burn_switch.is_open())

    def test__hold_temperature_level_while_requested(self):
        '''While requests exist, the buffer temperature should be kept at a
        predetermined level to ensure a constant flow.

        '''

        self.__brain.think('initial firing')
        self.assertTrue(self.__oil_burn_switch.is_closed())
        self.assertTrue(self.__oil_combo.is_requested_by(self.__sink))

        # oil buffer temperature well under its desired range -> still
        # heating
        self.__oil_thermometer.set_temperature(54)
        self.__brain.think('well below range')
        self.assertTrue(self.__oil_burn_switch.is_closed())

        # within range -> still heating
        self.__oil_thermometer.set_temperature(60)
        self.__brain.think('within range')
        self.assertTrue(self.__oil_burn_switch.is_closed())

        # above range -> heating off
        self.__oil_thermometer.set_temperature(76)
        self.__brain.think('above range')
        self.assertTrue(self.__oil_burn_switch.is_open())


class MinimumTemperatureTest(unittest.TestCase):
    def test__basic(self):
        brain = Brain()
        buffer_thermometer = TestThermometer(initial_temperature=20)
        burn_switch = TestSwitch(name='oil-burn', initial_state=False)
        oil_combo = OilCombo(
            name='my-oil-combo', 
            thermometer=buffer_thermometer, 
            burn_switch=burn_switch,
            heating_range=Hysteresis(60,70),
            minimum_temperature_range=Hysteresis(5,15),
            max_produced_temperature=90, # let's say
        )
        oil_combo.register_thinking(brain)

        # 20 degrees, no need to do anti-freeze
        brain.think('no need')
        self.assertTrue(burn_switch.is_open())

        # cool down -> anti-freeze starts
        buffer_thermometer.set_temperature(1)
        brain.think('frozen')
        self.assertTrue(burn_switch.is_closed())

        # reaching some temperature, but still not the upper bound of
        # the anti-freeze Hysteresis
        buffer_thermometer.set_temperature(10)
        brain.think('a little better')
        self.assertTrue(burn_switch.is_closed())

        # finally, it's time to stop anti-freeze
        buffer_thermometer.set_temperature(16)
        brain.think('finally thawed')
        self.assertTrue(burn_switch.is_open())
        

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(OilComboTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MinimumTemperatureTest))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
