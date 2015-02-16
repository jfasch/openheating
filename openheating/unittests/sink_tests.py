from openheating.testutils.thermometer import TestThermometer

from openheating.sink import Sink
from openheating.passive_source import PassiveSource
from openheating.thinking import Brain
from openheating.hysteresis import Hysteresis

import unittest
import logging

class SinkTest(unittest.TestCase):
    def test__basic(self):
        brain = Brain()

        sink_thermometer = TestThermometer(initial_temperature=10)
        sink = Sink(name='my-sink', thermometer=sink_thermometer,
                    hysteresis=Hysteresis(23, 27))
        source = PassiveSource(name='my-source', thermometer=None)
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


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
