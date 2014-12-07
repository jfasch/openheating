from openheating.sink import Sink
from openheating.source import Source
from openheating.thinking import Brain
from openheating.hysteresis import Hysteresis
from openheating.thermometer_dummy import DummyThermometer

import unittest
import logging

class SinkTest(unittest.TestCase):
    def test__basic(self):
        brain = Brain()

        sink_thermometer = DummyThermometer(initial_temperature=10)
        sink = Sink(name='my-sink', thermometer=sink_thermometer,
                    hysteresis=Hysteresis(23, 27))
        source = Source(name='my-source', thermometer=None)
        sink.set_source(source)
        brain.add(sink)

        # initial request
        brain.think()
        self.assertIn(sink, source.requesters())

        # heating up, right below lower hysteresis bound. still
        # requested
        sink_thermometer.set_temperature(22.9)
        brain.think()
        self.assertIn(sink, source.requesters())

        # heating up further, between low and high
        sink_thermometer.set_temperature(24)
        brain.think()
        self.assertIn(sink, source.requesters())

        # heating to the point where sink is satisfied
        sink_thermometer.set_temperature(27.1)
        brain.think()
        self.assertNotIn(sink, source.requesters())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SinkTest))

# suite.addTest(TransportBasicTest("test__pump_on_off_simple"))
# suite.addTest(TransportPeeksProducerTest("test__producer_not_peeked_when_consumer_satisfied"))

# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
