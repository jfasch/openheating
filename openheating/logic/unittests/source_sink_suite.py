from openheating.logic.brain import Brain
from openheating.logic.source import Source
from openheating.logic.sink import Sink
from openheating.logic.hysteresis import Hysteresis

from openheating.testutils.test_thermometer import TestThermometer
from openheating.testutils.test_switch import TestSwitch

import unittest
import logging

class _TestSource(Source):
    def __init__(self, name, thermometer):
        Source.__init__(self, name=name)
        self.__thermometer = thermometer
    def temperature(self):
        return self.__thermometer.temperature()

class _SourceSinkSuite(unittest.TestCase):
    def test__simplest(self):
        '''Building the structure. One source, one sink, both talk to each
        other.'''

        source_thermometer = TestThermometer(initial_temperature=20)
        source = _TestSource(name='source', thermometer=source_thermometer)

        sink_switch = TestSwitch(name='pump', initial_state=False)
        sink_thermometer = TestThermometer(initial_temperature=20)
        sink = Sink(name='sink', 
                    thermometer=sink_thermometer, 
                    temperature_range=Hysteresis(23, 30),
                    diff_hysteresis=Hysteresis(1,2), 
                    pump_switch=sink_switch)

        source.add_sink(sink)

        brain = Brain([source, sink])

        # sink 20, source 20. sink needs (>23), source has 20 -> pump
        # off.
        if True:
            sink_thermometer.set_temperature(20)
            source_thermometer.set_temperature(20)
            brain.think()
            self.assertEqual(sink_switch.get_state(), False)
            self.assertEqual(sink.test__get_need(), True)

        # sink 20, source 23. sink needs (>23), source has 23 -> pump
        # on.
        if True:
            sink_thermometer.set_temperature(20)
            source_thermometer.set_temperature(23)
            brain.think()
            self.assertEqual(sink_switch.get_state(), True)
            self.assertEqual(sink.test__get_need(), True)

        # sink 23, source 23.1. sink still needs because within range.
        if True:
            sink_thermometer.set_temperature(20)
            source_thermometer.set_temperature(23)
            brain.think()
            self.assertEqual(sink_switch.get_state(), True)
            self.assertEqual(sink.test__get_need(), True)

        self.fail()
        

suite = unittest.defaultTestLoader.loadTestsFromTestCase(_SourceSinkSuite)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
