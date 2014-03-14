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
    def test_basic(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(temperature=80)
        pump = TestPump()
        transport = Transport(producer=producer, consumer=consumer, pump=pump)

        transport.move()

        self.failUnless(pump.is_running())


suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportTest))
