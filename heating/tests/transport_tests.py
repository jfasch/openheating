from heating.tests.producers import TestProducer
from heating.tests.consumers import TestConsumer
from heating.tests.pumps import TestPump
from heating.tests.switches import TestSwitch

from heating.control.transport import Transport

import unittest
import logging

class TransportBasicTest(unittest.TestCase):
    def test__pump_on_off_simple(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(initial_temperature=80)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        # pump is off initially. switched on after first move, due to
        # difference of 40 degrees.
        self.failIf(pump.is_running())
        transport.move()
        self.failUnless(pump.is_running())

        # consumer reaches temperature, pump switched off. take into
        # account that we overheat by 7 degrees.
        consumer.set_temperature(40+7)
        transport.move()
        self.failIf(pump.is_running())

        # consumer's temperature falls by a lot of degrees (20 is a
        # lot), pump switched on again.
        consumer.set_temperature(20)        
        transport.move()
        self.failUnless(pump.is_running())

        # rises right below wanted, pump still running
        consumer.set_temperature(39)
        transport.move()
        self.failUnless(pump.is_running())

    def test_restart_delay(self):
        '''
        Consumer is satisfied with its temperature, pump not running
        initially. consumer's temperature falls, say, 1 degree below
        wanted, pump *not* switched on immediately.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=40)
        producer = TestProducer(initial_temperature=80)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()
        self.failIf(pump.is_running())

        consumer.set_temperature(39)
        transport.move()
        self.failIf(pump.is_running())

    def test__producer_below_wanted_but_pays_off(self):
        '''
        Producer's temperature is well below consumer's wanted temperature,
        but we take what we can get.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(initial_temperature=28)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=5, range_high=5, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()

        self.failUnless(pump.is_running())

    def test__producer_below_wanted_but_doesnt_pay_off(self):
        '''
        Producer's temperature is well below consumer's wanted temperature,
        and it does not pay off to take this small amount of temperature.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(initial_temperature=21)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()

        self.failIf(pump.is_running())

    def test__producer_has_nothing__pump_not_initially_running(self):
        '''
        Consumer is unsatisfied. producer has nothing to satisfy
        him. pump *is not* initially running, and *is not* switched
        on.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(initial_temperature=20)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()
        self.failIf(pump.is_running())

    def test__producer_has_nothing__pump_initially_running(self):
        '''
        Consumer is unsatisfied. producer has nothing to satisfy
        him. pump *is* initially running, and *is switched off*.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(initial_temperature=20)
        pump = TestPump(running=True)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()
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
        producer = TestProducer(initial_temperature=20)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()

        self.failIf(producer.is_acquired())
        
    def test__producer_not_acquired_when_producer_has_enough_temperature(self):
        '''
        Producer's temperature is enough to satisfy consumer.
        Producer not acquired.
        '''
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=20)
        producer = TestProducer(initial_temperature=80)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()

        self.failIf(producer.is_acquired())
        
    def test__producer_acquired_when_consumer_not_satisfied(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=30)
        producer = TestProducer(initial_temperature=20)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=TestSwitch(on=False))

        transport.move()

        self.failIf(pump.is_running())
        self.failUnless(producer.is_acquired())

        producer.set_temperature(70)

        transport.move()

        self.failUnless(pump.is_running())
        self.failUnless(producer.is_acquired())

        consumer.set_temperature(47)

        transport.move()

        self.failIf(pump.is_running())
        self.failIf(producer.is_acquired())

class TransportProducerNeedsCoolingTest(unittest.TestCase):
    '''
    A producer can flag that he needs cooling.
    No matter what the consumer says, heat is being transported in this case.
    Provided that the consumer's temperature is not higher than the producer's,
    of course - in this case an alarm is raised.
    '''
    
    def test__producer_needs_cooling(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=48)
        producer = TestProducer(initial_temperature=100)
        pump = TestPump(running=False)
        alarm_switch = TestSwitch(on=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump,
                              alarm_switch=alarm_switch)

        transport.move()

        # producer is left alone because consumer is all
        # satisfied. 100 degrees don't matter unless producer flags an
        # emergency condition.
        self.failIf(producer.is_acquired())
        self.failIf(pump.is_running())

        # flag emergency condition
        producer.set_needs_cooling(True)

        transport.move()

        self.failIf(producer.is_acquired())
        self.failUnless(pump.is_running())

        # cooling did help, temperatures are equal now. anyway,
        # producer still needs cooling -> ALARM rings
        producer.set_temperature(60)
        consumer.set_temperature(60)

        transport.move()

        self.failIf(producer.is_acquired())
        self.failIf(pump.is_running())
        self.failUnless(alarm_switch.is_on())

        # no cooling needed anymore -> alarm off
        producer.set_needs_cooling(False)
        
        transport.move()

        self.failIf(alarm_switch.is_on())
        self.failIf(pump.is_running())
        self.failIf(producer.is_acquired())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportBasicTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportAcquireReleaseProducerTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportProducerNeedsCoolingTest))

# suite.addTest(TransportBasicTest("test__pump_on_off_simple"))
# suite.addTest(TransportPeeksProducerTest("test__producer_not_peeked_when_consumer_satisfied"))

# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
