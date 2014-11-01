from openheating.tests.producers import TestProducerBackend
from openheating.tests.consumers import TestConsumer
from openheating.tests.pumps import TestPump
from openheating.tests.switches import TestSwitch

from openheating.producer import Producer
from openheating.transport import Transport

import unittest
import logging

class TransportBasicTest(unittest.TestCase):
    def test__pump_on_off_simple(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer_backend = TestProducerBackend(initial_temperature=80)
        producer = Producer(name='Producer', backend=producer_backend,
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        # pump is off initially. switched on after first move, due to
        # difference of 40 degrees.
        self.failIf(pump.is_running())
        transport.poll()
        self.failUnless(pump.is_running())

        # consumer reaches temperature, pump switched off. take into
        # account that we overheat by 7 degrees.
        consumer.set_temperature(40+7)
        transport.poll()
        self.failIf(pump.is_running())

        # consumer's temperature falls by a lot of degrees (20 is a
        # lot), pump switched on again.
        consumer.set_temperature(20)        
        transport.poll()
        self.failUnless(pump.is_running())

        # rises right below wanted, pump still running
        consumer.set_temperature(39)
        transport.poll()
        self.failUnless(pump.is_running())

    def test_restart_delay(self):
        '''
        Consumer is satisfied with its temperature, pump not running
        initially. consumer's temperature falls, say, 1 degree below
        wanted, pump *not* switched on immediately.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=40)
        producer = Producer(name='Producer', backend=TestProducerBackend(initial_temperature=80),
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        transport.poll()
        self.failIf(pump.is_running())

        consumer.set_temperature(39)
        transport.poll()
        self.failIf(pump.is_running())

    def test__producer_below_wanted_but_pays_off(self):
        '''
        Producer's temperature is well below consumer's wanted temperature,
        but we take what we can get.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = Producer(name='Producer', backend=TestProducerBackend(initial_temperature=28),
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=5, range_high=5, pump=pump)

        transport.poll()

        self.failUnless(pump.is_running())

    def test__producer_below_wanted_but_doesnt_pay_off(self):
        '''
        Producer's temperature is well below consumer's wanted temperature,
        and it does not pay off to take this small amount of temperature.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = Producer(name='Producer', backend=TestProducerBackend(initial_temperature=21),
                            overheat_temperature=100, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        transport.poll()

        self.failIf(pump.is_running())

    def test__producer_has_nothing__pump_not_initially_running(self):
        '''
        Consumer is unsatisfied. producer has nothing to satisfy
        him. pump *is not* initially running, and *is not* switched
        on.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = Producer(name='Producer', backend=TestProducerBackend(initial_temperature=20),
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        transport.poll()
        self.failIf(pump.is_running())

    def test__producer_has_nothing__pump_initially_running(self):
        '''
        Consumer is unsatisfied. producer has nothing to satisfy
        him. pump *is* initially running, and *is switched off*.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = Producer(name='Producer', backend=TestProducerBackend(initial_temperature=20),
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=True)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        transport.poll()
        self.failIf(pump.is_running())

class TransportAcquireReleaseProducerTest(unittest.TestCase):
    '''
    Transport coordinates between consumer's needs and a producer.
    It can peek the producer to make some temperature if the consumer needs it.
    '''
    
    def test__producer_not_acquired_when_consumer_satisfied(self):
        '''
        Simplest thing: when nobody needs anything,
        then we don't produce
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=48)
        producer = Producer(name='Producer', backend=TestProducerBackend(initial_temperature=20),
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        transport.poll()

        self.failIf(producer.is_acquired())
        
    def test__producer_not_acquired_when_producer_has_enough_temperature(self):
        '''
        Producer's temperature is enough to satisfy consumer.
        Producer not acquired.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = Producer(name='Producer', backend=TestProducerBackend(initial_temperature=80),
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        transport.poll()

        self.failIf(producer.is_acquired())
        
    def test__producer_acquired_when_consumer_not_satisfied(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=30)
        producer_backend = TestProducerBackend(initial_temperature=20)
        producer = Producer(name='Producer', backend=producer_backend,
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        transport.poll()

        self.failIf(pump.is_running())
        self.failUnless(producer.is_acquired())

        producer_backend.set_temperature(70)

        transport.poll()

        self.failUnless(pump.is_running())
        self.failUnless(producer.is_acquired())

        consumer.set_temperature(47)

        transport.poll()

        self.failIf(pump.is_running())
        self.failIf(producer.is_acquired())

    def test__producer_with_two_consumers__synchronous(self):
        '''
        Two consumers are attached to a producer. Both consumers
        reach their desired temperature level at the same time.
        '''

        producer_backend = TestProducerBackend(initial_temperature=20)
        producer = Producer(name='Producer', backend=producer_backend,
                            overheat_temperature=1000, alarm_switch=TestSwitch(on=False))

        consumerA = TestConsumer(wanted_temperature=40, initial_temperature=30)
        pumpA = TestPump(running=False)
        transportA = Transport(name='Transport-A', producer=producer, consumer=consumerA, range_low=7, range_high=7, pump=pumpA)

        consumerB = TestConsumer(wanted_temperature=40, initial_temperature=30)
        pumpB = TestPump(running=False)
        transportB = Transport(name='Transport-B', producer=producer, consumer=consumerB, range_low=7, range_high=7, pump=pumpB)

        transportA.poll()
        transportB.poll()

        # not yet hot enough ...
        self.failIf(pumpA.is_running())
        self.failIf(pumpB.is_running())

        # ... though heat is underway
        self.failUnless(producer.is_acquired())

        # heat is coming
        producer_backend.set_temperature(70)

        transportA.poll()
        transportB.poll()

        self.failUnless(pumpA.is_running())
        self.failUnless(pumpB.is_running())
        self.failUnless(producer.is_acquired())

        consumerA.set_temperature(47)
        consumerB.set_temperature(47)

        transportA.poll()
        transportB.poll()

        self.failIf(pumpA.is_running())
        self.failIf(pumpB.is_running())
        self.failIf(producer.is_acquired())

    def test__producer_with_two_consumers__asynchronous(self):
        '''
        Two consumers are attached to a producer. One consumer reaches
        its temperature level, while the other keeps wanting.
        '''

        producer_backend = TestProducerBackend(initial_temperature=20)
        producer = Producer(name='Producer', backend=producer_backend, overheat_temperature=1000, alarm_switch=TestSwitch(on=False))

        consumerA = TestConsumer(wanted_temperature=40, initial_temperature=30)
        pumpA = TestPump(running=False)
        transportA = Transport(name='Transport-A', producer=producer, consumer=consumerA, range_low=7, range_high=7, pump=pumpA)

        consumerB = TestConsumer(wanted_temperature=40, initial_temperature=30)
        pumpB = TestPump(running=False)
        transportB = Transport(name='Transport-B', producer=producer, consumer=consumerB, range_low=7, range_high=7, pump=pumpB)

        transportA.poll()
        transportB.poll()

        # not yet hot enough ...
        self.failIf(pumpA.is_running())
        self.failIf(pumpB.is_running())

        # ... though heat is underway
        self.failUnless(producer.is_acquired())
        self.failUnless(len(producer.get_acquirers()) == 2)
        self.failUnless('Transport-A' in producer.get_acquirers())
        self.failUnless('Transport-B' in producer.get_acquirers())

        # heat is coming
        producer_backend.set_temperature(70)

        transportA.poll()
        transportB.poll()

        self.failUnless(pumpA.is_running())
        self.failUnless(pumpB.is_running())
        self.failUnless(producer.is_acquired())
        self.failUnless(len(producer.get_acquirers()) == 2)
        self.failUnless('Transport-A' in producer.get_acquirers())
        self.failUnless('Transport-B' in producer.get_acquirers())

        # A is satisfied
        consumerA.set_temperature(47)

        transportA.poll()
        transportB.poll()

        # A down, B still wants more
        self.failIf(pumpA.is_running())
        self.failUnless(pumpB.is_running())
        self.failUnless(producer.is_acquired())
        self.failUnless(len(producer.get_acquirers()) == 1)
        self.failUnless('Transport-B' in producer.get_acquirers())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportBasicTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportAcquireReleaseProducerTest))

# suite.addTest(TransportBasicTest("test__pump_on_off_simple"))
# suite.addTest(TransportPeeksProducerTest("test__producer_not_peeked_when_consumer_satisfied"))

# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
