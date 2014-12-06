from openheating.sink import Sink
from openheating.source import Source
from openheating.polling import Poller
from openheating.hysteresis import Hysteresis
from openheating.thermometer_dummy import DummyThermometer

import unittest
import logging

class SinkTest(unittest.TestCase):
    def test__basic(self):
        poller = Poller(num_polls=2)

        sink_thermometer = DummyThermometer(initial_temperature=10)
        sink = Sink(name='my-sink', thermometer=sink_thermometer,
                    hysteresis=Hysteresis(23, 27))
        source = Source(name='my-source', thermometer=None)
        sink.set_source(source)
        poller.add(sink)

        # initial request
        poller.poll()
        self.assertIn(sink, source.requesters())

        # heating up, right below lower hysteresis bound. still
        # requested
        sink_thermometer.set_temperature(22.9)
        poller.poll()
        self.assertIn(sink, source.requesters())

        # heating up further, between low and high
        sink_thermometer.set_temperature(24)
        poller.poll()
        self.assertIn(sink, source.requesters())

        # heating to the point where sink is satisfied
        sink_thermometer.set_temperature(27.1)
        poller.poll()
        self.assertNotIn(sink, source.requesters())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SinkTest))

# suite.addTest(TransportBasicTest("test__pump_on_off_simple"))
# suite.addTest(TransportPeeksProducerTest("test__producer_not_peeked_when_consumer_satisfied"))

# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
