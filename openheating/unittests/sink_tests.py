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
                    temperature_range=Hysteresis(23, 27))
        source = PassiveSource(
            name='my-source', 
            thermometer=None,
            max_produced_temperature=1000, # don't care
        )
        sink.set_source(source)

        sink.register_thinking(brain)
        source.register_thinking(brain)

        # initial request
        brain.think()
        self.assertTrue(source.is_requested_by(sink))

        # heating up, right below lower hysteresis bound. still
        # requested
        sink_thermometer.set_temperature(22.9)
        brain.think()
        self.assertTrue(source.is_requested_by(sink))

        # heating up further, between low and high
        sink_thermometer.set_temperature(24)
        brain.think('heating up further')
        self.assertTrue(source.is_requested_by(sink))

        # heating to the point where sink is satisfied
        sink_thermometer.set_temperature(27.1)
        brain.think()
        self.assertFalse(source.is_requested_by(sink))

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SinkTest))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
