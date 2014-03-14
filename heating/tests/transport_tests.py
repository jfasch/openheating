from ..control.transport import Transport
from ..control.consumer import Consumer
from ..control.producer import Producer
from ..control.pump import Pump

import unittest

class TestConsumer(Consumer):
    def __init__(self, wanted_temperature, initial_temperature):
        self.__wanted_temperature = wanted_temperature
        self.__temperature = initial_temperature
    def temperature(self):
        return self.__temperature
    def wanted_temperature(self):
        return self.__wanted_temperature
    def set_temperature(self, temperature):
        self.__temperature = temperature

class TestProducer(Producer):
    def __init__(self, temperature):
        self.__temperature = temperature
    def temperature(self):
        return self.__temperature

class TestPump(Pump):
    def __init__(self):
        self.__is_running = False
    def is_running(self):
        return self.__is_running
    def start(self):
        self.__is_running = True
    def stop(self):
        self.__is_running = False

class TransportTest(unittest.TestCase):
    def test_pump_on_off_simple(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(temperature=80)
        pump = TestPump()
        transport = Transport(producer=producer, consumer=consumer, anti_oscillating_threshold=7, pump=pump)

        # pump is off initially. switched on after first move, due to
        # difference of 40 degrees.
        self.failIf(pump.is_running())
        transport.move()
        self.failUnless(pump.is_running())

        # consumer reaches temperature, pump switched off
        consumer.set_temperature(40)
        transport.move()
        self.failIf(pump.is_running())

        # consumer's temperature falls by a lot of degrees (20 is a
        # lot), pump switched on again.
        consumer.set_temperature(20)        
        transport.move()
        self.failUnless(pump.is_running())

    def test_restart_delay(self):
        # consumer is satisfied with its temperature, pump not running
        # initially. consumer's temperature falls, say, 1 degree below
        # wanted, pump *not* switched on immediately.
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=40)
        producer = TestProducer(temperature=80)
        pump = TestPump()
        transport = Transport(producer=producer, consumer=consumer, anti_oscillating_threshold=7, pump=pump)

        transport.move()
        self.failIf(pump.is_running())

        consumer.set_temperature(39)
        transport.move()
        self.failIf(pump.is_running())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportTest))
