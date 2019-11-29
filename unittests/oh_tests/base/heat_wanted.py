from openheating.base.switch import DummySwitch
from openheating.base.thermometer import DummyThermometer
from openheating.base.circuit import Circuit
from openheating.base.hysteresis import Hysteresis

import unittest
import logging
import itertools


class SimpleBuffer:
    def __init__(self, name, thermometer, circuit, low, high):
        self.__name = name
        self.__satisfied = True   # initially quiet
        self.__thermometer = thermometer
        self.__circuit = circuit

        self.__hysteresis = Hysteresis(
            name='Hysteresis({})'.format(name),
            low=low,
            high=high,
            below_low=self._dont_be_satisfied,
            above_high=self._be_satisfied)

    def is_satisfied(self):
        return self.__satisfied

    def poll(self, timestamp):
        logging.debug('{}: poll({})'.format(self.__name, timestamp))

        self.__hysteresis(timestamp, self.__thermometer.get_temperature())

        if self.__satisfied:
            self.__circuit.deactivate()
        else:
            self.__circuit.activate()

    def _be_satisfied(self):
        if not self.__satisfied:
            logging.debug('{}: now satisfied'.format(self.__name))
            self.__satisfied = True

    def _dont_be_satisfied(self):
        if self.__satisfied:
            logging.debug('{}: not anymore satisfied'.format(self.__name))
            self.__satisfied = False

class Poller:
    def __init__(self, timestamps, pollables=None):
        self.__pollables = pollables
        self.__timiter = iter(timestamps)

    def poll_n(self, n, msg=None):
        dmsg = 'poll {} times'.format(n)
        if msg:
            dmsg += ': ' + msg
        logging.debug(dmsg)
        while n > 0:
            ts = next(self.__timiter)
            self.__poll(ts)
            n -= 1

    def __poll(self, timestamp):
        for p in self.__pollables:
            p.poll(timestamp)

class HeatWantedTest(unittest.TestCase):
    def setUp(self):
        self.__pump = DummySwitch('pump', 'some pump', False)
        self.__heater_thermometer = DummyThermometer('heater', 'some heater', 10)
        self.__buffer_thermometer = DummyThermometer('buffer', 'some buffer', 10)

        self.__circuit = Circuit(
            name='testcircuit',
            pump=self.__pump,
            producer=self.__heater_thermometer,
            consumer=self.__buffer_thermometer,
            diff_low=2,
            diff_high=4)

        self.__buffer = SimpleBuffer(
            name = 'testbuffer',
            thermometer=self.__buffer_thermometer,
            circuit=self.__circuit,
            low=40,
            high=65)

        self.__poller = Poller(timestamps=itertools.count(0, 5),
                               pollables=[self.__circuit, self.__buffer])

    def test__consumer_starts_wanting(self):
        # too cold, well below hysteresis.low -> activate circuit
        self.assertFalse(self.__circuit.is_active())
        self.__poller.poll_n(5, 'initial, activating circuit')
        self.assertTrue(self.__circuit.is_active())

        # another round to take the pump/circuit into consideration
        self.__poller.poll_n(5, 'still cold, pump still off')
        # circuit see 10 degrees on either side, so pump is off.
        self.assertFalse(self.__pump.get_state())

        # now turn on the oven
        self.__heater_thermometer.set_temperature(30)
        self.__poller.poll_n(5, 'heating up, pump goes on')
        # pump is running
        self.assertTrue(self.__pump.get_state())

    def test__consumer_satisfied(self):
        self.__heater_thermometer.set_temperature(80)
        self.__poller.poll_n(5, 'heating up')
        self.assertTrue(self.__pump.get_state())
        
        # buffer gains temperature, well above its higher bound
        self.__buffer_thermometer.set_temperature(80)
        self.__poller.poll_n(5)

        # buffer satisfied -> circuit deactivated
        self.assertTrue(self.__buffer.is_satisfied())
        self.assertFalse(self.__circuit.is_active())
        self.assertFalse(self.__pump.get_state())

    def test__pump_off_when_circuit_deactivated(self):
        self.__heater_thermometer.set_temperature(80)
        self.__poller.poll_n(5, 'heating up')
        self.assertTrue(self.__pump.get_state())
        self.assertTrue(self.__circuit.is_active())

        # circuit deactivated outside of buffer's control.
        self.__circuit.deactivate()
        self.assertFalse(self.__circuit.is_active())
        self.assertFalse(self.__pump.get_state())

        # buffer parameters remain unchanged. he continues crying for
        # heat, which is why the circuit goes on again.
        self.__poller.poll_n(5)
        self.assertTrue(self.__circuit.is_active())
        self.assertTrue(self.__pump.get_state())
        

suite = unittest.defaultTestLoader.loadTestsFromTestCase(HeatWantedTest)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
