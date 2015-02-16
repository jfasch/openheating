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
        self.__sink = Sink(name='my-sink', thermometer=self.__sink_thermometer, hysteresis=Hysteresis(low=40, high=45))
        self.__brain.add(self.__sink)

        self.__oil_thermometer = TestThermometer(initial_temperature=20)
        self.__oil_burn_switch = TestSwitch(name='oil-burn', initial_state=False)

        self.__oil_combo = OilCombo(name='my-oil-combo', thermometer=self.__oil_thermometer,
                                    burn_switch=self.__oil_burn_switch,
                                    anti_freeze=Hysteresis(1,2))

        self.__transport = Transport(name='my-transport',
                                     source=self.__oil_combo, sink=self.__sink,
                                     diff_hysteresis=Hysteresis(0, 5),
                                     pump_switch=TestSwitch(name='pump', initial_state=False))
        self.__brain.add(self.__transport)
        self.__brain.add(self.__oil_combo)

    def test__initial_state(self):
        # no action unless explicitly stated
        self.assertTrue(self.__oil_burn_switch.is_open())

    def test__request_by_sink(self):
        self.assertTrue(self.__oil_burn_switch.is_open())

        # sink is way below wanted, so after thinking oil must be
        # requested
        self.__brain.think()
        self.assertIn(self.__sink, self.__oil_combo.requesters())

        # sink requests -> burn-switch is closed
        self.assertTrue(self.__oil_burn_switch.is_closed())

    def test__release_by_sink(self):
        self.assertTrue(self.__oil_burn_switch.is_open())
        
        # sink is way below wanted, so after thinking oil must be
        # requested
        self.__brain.think()
        self.assertIn(self.__sink, self.__oil_combo.requesters())
        self.assertTrue(self.__oil_burn_switch.is_closed())

        # sink temperature rises above wanted -> release
        self.__sink_thermometer.set_temperature(50)
        self.__brain.think()
        self.assertNotIn(self.__sink, self.__oil_combo.requesters())
        self.assertTrue(self.__oil_burn_switch.is_open())


class AntiFreezeTest(unittest.TestCase):
    def test__basic(self):
        brain = Brain()
        buffer_thermometer = TestThermometer(initial_temperature=20)
        burn_switch = TestSwitch(name='oil-burn', initial_state=False)
        oil_combo = OilCombo(
            name='my-oil-combo', 
            thermometer=buffer_thermometer, 
            burn_switch=burn_switch,
            anti_freeze=Hysteresis(5,15))
        brain.add(oil_combo)

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
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(AntiFreezeTest))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
