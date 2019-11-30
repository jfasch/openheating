from openheating.base.switch import DummySwitch
from openheating.base.thermometer import DummyThermometer
from openheating.base.circuit import Circuit
from openheating.base.error import ClockSkewError

import unittest
import datetime


class CircuitTest(unittest.TestCase):

    def setUp(self):
        self.__pump = DummySwitch('pump', 'some pump', False)
        self.__producer = DummyThermometer('producer', 'some producer', 10)
        self.__consumer = DummyThermometer('consumer', 'some consumer', 10)
        self.__circuit = Circuit(
            name='name',
            pump=self.__pump,
            producer=self.__producer,
            consumer=self.__consumer,
            diff_low=2,
            diff_high=4)

    def test__basic(self):
        self.__circuit.activate()

        self.assertTrue(self.__circuit.is_active())

        # diff 0
        self.__circuit.poll(0)
        self.assertFalse(self.__pump.get_state())

        # diff > 4 (high)
        self.__producer.set_temperature(14.5)
        self.__circuit.poll(1)
        self.assertTrue(self.__pump.get_state())

        # 2 < diff < 4
        self.__consumer.set_temperature(12)
        self.__circuit.poll(1)
        self.assertTrue(self.__pump.get_state()) # unchanged

        # diff < 2
        self.__producer.set_temperature(12.3)
        self.__circuit.poll(1)
        self.assertFalse(self.__pump.get_state())

    def test__look__takes_datetime_and_timestamp(self):
        self.__circuit.activate()

        self.__circuit.poll(0) # epoch
        self.__circuit.poll(datetime.datetime.fromtimestamp(1)) # epoch+1

    def test__complain_clock_skew(self):
        self.__circuit.activate()

        self.__circuit.poll(1)
        with self.assertRaises(ClockSkewError):
            self.__circuit.poll(0)

    def test__look_does_nothing_when_inactive(self):
        self.assertFalse(self.__circuit.is_active())
        self.__circuit.deactivate() # nop
        self.assertFalse(self.__circuit.is_active())

        self.__producer.set_temperature(50)
        self.__consumer.set_temperature(10) # considerable diff
        self.__circuit.poll(42)

        self.assertFalse(self.__pump.get_state())

suite = unittest.defaultTestLoader.loadTestsFromTestCase(CircuitTest)

if __name__ == '__main__':
    unittest.main()
