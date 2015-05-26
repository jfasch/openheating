from openheating.testutils.test_thermometer import TestThermometer

from openheating.logic.sink import Sink
from openheating.logic.passive_source import PassiveSource
from openheating.logic.brain import Brain
from openheating.logic.hysteresis import Hysteresis

import unittest
import logging


class SinkTest(unittest.TestCase):
    def test__basic(self):
        sink_thermometer = TestThermometer(initial_temperature=10)
        sink = Sink(name='my-sink', thermometer=sink_thermometer,
                    temperature_range=Hysteresis(23, 27))
        source = PassiveSource(
            name='my-source', 
            thermometer=TestThermometer(initial_temperature=0),
            max_produced_temperature=1000, # don't care
        )
        sink.set_source(source)

        brain = Brain([source, sink])


        # initial request
        brain.think('initial request')
        self.assertTrue(source.is_requested_by(sink))

        # heating up, right below lower hysteresis bound. still
        # requested
        sink_thermometer.set_temperature(22.9)
        brain.think('heating up until below hysteresis')
        self.assertTrue(source.is_requested_by(sink))

        # heating up further, between low and high
        sink_thermometer.set_temperature(24)
        brain.think('heating up further')
        self.assertTrue(source.is_requested_by(sink))

        # heating to the point where sink is satisfied
        sink_thermometer.set_temperature(27.1)
        brain.think('satisfied')
        self.assertFalse(source.is_requested_by(sink))

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SinkTest))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
