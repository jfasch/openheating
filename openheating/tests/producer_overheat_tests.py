from openheating.tests.producers import TestProducerBackend
from openheating.tests.consumers import TestConsumer
from openheating.tests.pumps import TestPump
from openheating.tests.switches import TestSwitch
from openheating.tests.poller import TestPoller

from openheating.producer import Producer
from openheating.transport import Transport

import logging
import unittest

class TransportProducerNeedsCoolingTest(unittest.TestCase):
    '''
    Producer overheat condition.
    Even if the consumer is satisfied, heat is being transported in this case.
    Provided that the consumer's temperature is not higher than the producer's,
    of course - in this case an alarm is raised.
    '''
    
    def test__producer_needs_cooling__single_consumer(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=48)
        producer_backend = TestProducerBackend(initial_temperature=70)
        alarm_switch = TestSwitch(on=False)
        producer = Producer(name='Producer', backend=producer_backend, overheat_temperature=100, alarm_switch=alarm_switch)
        pump = TestPump(running=False)
        transport = Transport(name='xxx', producer=producer, consumer=consumer, range_low=7, range_high=7, pump=pump)

        # first round, all easy
        if True:
            transport.poll()

            # producer is left alone because consumer is all
            # satisfied, and producer is not yet overheating
            self.failIf(producer.is_acquired())
            self.failIf(pump.is_running())
            self.failIf(alarm_switch.is_on())

        # producer's temperature rises -> overheating
        if True:
            producer_backend.set_temperature(101)

            transport.poll()

            self.failIf(producer.is_acquired())
            self.failUnless(pump.is_running())
            self.failIf(alarm_switch.is_on())

        # consumer is satisfied, but is forced to give cooling. still
        # no alarm because producer is being cooled.
        if True:
            consumer.set_temperature(80)

            transport.poll()

            self.failIf(producer.is_acquired())
            self.failUnless(pump.is_running())
            self.failIf(alarm_switch.is_on())

        # no cooling needed anymore -> alarm off
        if True:
            producer_backend.set_temperature(90)
        
            transport.poll()

            self.failIf(alarm_switch.is_on())
            self.failIf(pump.is_running())
            self.failIf(producer.is_acquired())

    def test__producer_needs_cooling__multiple_consumers(self):
        alarm_switch = TestSwitch(on=False)
        
        producer_backend = TestProducerBackend(initial_temperature=80)
        producer = Producer(name='Producer', backend=producer_backend, overheat_temperature=90, alarm_switch=alarm_switch)

        consumerA = TestConsumer(wanted_temperature=40, initial_temperature=48)
        pumpA = TestPump(running=False)
        transportA = Transport(name='A', producer=producer, consumer=consumerA, range_low=7, range_high=7, pump=pumpA)

        consumerB = TestConsumer(wanted_temperature=40, initial_temperature=48)
        pumpB = TestPump(running=False)
        transportB = Transport(name='B', producer=producer, consumer=consumerB, range_low=7, range_high=7, pump=pumpB)

        poller = TestPoller([transportA, transportB, producer])

        self.failUnless(len(producer.get_transports()) == 2)
        self.failUnless(transportA in producer.get_transports())
        self.failUnless(transportB in producer.get_transports())

        # everybody satisfied, everything easy
        if True:
            poller.poll()

            self.failIf(pumpA.is_running())
            self.failIf(pumpB.is_running())
            self.failIf(producer.is_acquired())


        # producer about to explode
        if True:
            producer_backend.set_temperature(90)
        
            poller.poll()

            # both transports must be running ...
            self.failUnless(pumpA.is_running())
            self.failUnless(pumpB.is_running())
            # ... although nobody explicitly demanded heating
            self.failIf(producer.is_acquired())
            # no need to flag alarm since cooling is underway
            self.failIf(alarm_switch.is_on())


        # consumer A cannot make it anymore, its temperature and
        # producer's become equal
        if True:
            consumerA.set_temperature(90)

            poller.poll()

            # A off, B still in cooling mode.
            self.failIf(pumpA.is_running())
            self.failUnless(pumpB.is_running())
            # still nobody wants heat.            
            self.failIf(producer.is_acquired())
            # still no need to flag alarm
            self.failIf(alarm_switch.is_on())

        # now consumer B cannot take it anymore
        if True:
            consumerB.set_temperature(90)
        
            poller.poll()

            # no cooling, producer still cries bloody murder -> alarm
            self.failIf(pumpA.is_running())
            self.failIf(pumpB.is_running())
            self.failUnless(alarm_switch.is_on())
            self.failIf(producer.is_acquired())

        # consumer A manages to lose some temperature
        if True:
            consumerA.set_temperature(30)

            poller.poll()

            # alarm off, cooling in progress
            self.failIf(alarm_switch.is_on())
            self.failIf(pumpB.is_running())
            self.failUnless(pumpA.is_running())
            self.failIf(producer.is_acquired())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportProducerNeedsCoolingTest))
#suite.addTest(TransportProducerNeedsCoolingTest("test__producer_needs_cooling__multiple_consumers"))

#logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
