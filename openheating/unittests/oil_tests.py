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
        self.__oil_enable_switch = TestSwitch(name='oil-enable', initial_state=False)
        self.__oil_burn_switch = TestSwitch(name='oil-burn', initial_state=False)

        self.__oil_combo = OilCombo(name='my-oil-combo', thermometer=self.__oil_thermometer,
                                    enable_switch=self.__oil_enable_switch, burn_switch=self.__oil_burn_switch)

        self.__transport = Transport(name='my-transport',
                                     source=self.__oil_combo, sink=self.__sink,
                                     diff_hysteresis=Hysteresis(0, 5),
                                     pump_switch=TestSwitch(name='pump', initial_state=False))
        self.__brain.add(self.__transport)

    def test__initial_state(self):
        # no action unless explicitly stated
        self.assertTrue(self.__oil_enable_switch.is_open())
        self.assertTrue(self.__oil_burn_switch.is_open())

        # enable combo
        if True:
            self.__oil_combo.enable()
            self.assertTrue(self.__oil_enable_switch.is_closed())        
            self.assertTrue(self.__oil_burn_switch.is_open())

        # disable combo
        if True:
            self.__oil_combo.disable()
            self.assertTrue(self.__oil_enable_switch.is_open())
            self.assertTrue(self.__oil_burn_switch.is_open())

    def test__request_by_sink(self):
        self.__oil_combo.enable()
        self.assertTrue(self.__oil_burn_switch.is_open())

        # sink is way below wanted, so after thinking oil must be
        # requested
        self.__brain.think()
        self.assertIn(self.__sink, self.__oil_combo.requesters())

        # sink requests -> burn-switch is closed
        self.assertTrue(self.__oil_burn_switch.is_closed())

    def test__release_by_sink(self):
        self.__oil_combo.enable()
        self.assertTrue(self.__oil_burn_switch.is_open())
        
        # sink is way below wanted, so after thinking oil must be
        # requested
        self.__brain.think()
        self.assertIn(self.__sink, self.__oil_combo.requesters())
        self.assertTrue(self.__oil_burn_switch.is_closed())
        self.assertTrue(self.__oil_enable_switch.is_closed())

        # sink temperature rises above wanted -> release
        self.__sink_thermometer.set_temperature(50)
        self.__brain.think()
        self.assertNotIn(self.__sink, self.__oil_combo.requesters())
        self.assertTrue(self.__oil_burn_switch.is_open())
        self.assertTrue(self.__oil_enable_switch.is_closed())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(OilComboTest))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
