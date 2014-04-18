from heating.control.producer import Producer
from heating.tests.producers import TestProducerBackend
from heating.tests.consumers import TestConsumer
from heating.tests.pumps import TestPump
from heating.tests.switches import TestSwitch

from heating.control.transport import Transport

import unittest

class TransportProducerNeedsCoolingTest(unittest.TestCase):
    '''
    A producer can flag that he needs cooling.
    No matter what the consumer says, heat is being transported in this case.
    Provided that the consumer's temperature is not higher than the producer's,
    of course - in this case an alarm is raised.
    '''
    
    def test__producer_needs_cooling(self):
        consumer = TestConsumer(wanted_temperature=40, initial_temperature=48)
        producer_backend = TestProducerBackend(initial_temperature=100)
        producer = Producer(backend=producer_backend)
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
        producer_backend.set_needs_cooling(True)

        transport.move()

        self.failIf(producer.is_acquired())
        self.failUnless(pump.is_running())

        # cooling did help, temperatures are equal now. anyway,
        # producer still needs cooling -> ALARM rings
        producer_backend.set_temperature(60)
        consumer.set_temperature(60)

        transport.move()

        self.failIf(producer.is_acquired())
        self.failIf(pump.is_running())
        self.failUnless(alarm_switch.is_on())

        # no cooling needed anymore -> alarm off
        producer_backend.set_needs_cooling(False)
        
        transport.move()

        self.failIf(alarm_switch.is_on())
        self.failIf(pump.is_running())
        self.failIf(producer.is_acquired())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportProducerNeedsCoolingTest))

# suite.addTest(TransportProducerNeedsCoolingTest("test__producer_needs_cooling"))

# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
