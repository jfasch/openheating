from openheating.tests.switches import TestSwitch


from openheating.polling import Poller
from openheating.thermometer_dummy import DummyThermometer
from openheating.source import Source
from openheating.sink import Sink
from openheating.hysteresis import Hysteresis
from openheating.transport import Transport

import unittest
import logging

class TransportBasicTest(unittest.TestCase):
    def test__basic(self):
        poller = Poller()
        
        sink_thermometer = DummyThermometer(initial_temperature=20)
        sink = Sink(name='my-sink', thermometer=sink_thermometer,
                    hysteresis=Hysteresis(33, 47))
        poller.add(sink)

        source_thermometer = DummyThermometer(initial_temperature=80)
        source = Source(name='my-source', thermometer=source_thermometer)

        pump_switch = TestSwitch(on=False)
        transport = Transport(name='my-transport', source=source, sink=sink,
                              diff_hysteresis=Hysteresis(0, 5),
                              pump_switch=pump_switch)
        poller.add(transport)

        # pump is off initially. switched on after first move, due to
        # difference of 60 degrees. sink is far below its desired
        # temperature, so it explicitly requests heating
        if True:
            self.assertFalse(pump_switch.is_on())
            poller.poll('initial, diff is huge, request')
            self.assertTrue(pump_switch.is_on())
            self.assertIn(sink, source.requesters())

        # sink reaches its desired temperature. pump is kept running
        # nonetheless - it's the temperature difference which
        # matters. no heating explicitly requested anymore though.
        if True:
            sink_thermometer.set_temperature(50)
            poller.poll('sink satisfied, diff still there')
            self.assertTrue(pump_switch.is_on())
            self.assertNotIn(sink, source.requesters())

        # source's temperature falls to 55.1. this makes a temperature
        # difference of 5.1. threshold is 5, so pump is kept running.
        if True:
            source_thermometer.set_temperature(55.1)
            poller.poll('source cools, still some diff')
            self.assertTrue(pump_switch.is_on())
            self.assertNotIn(sink, source.requesters())
            
        # source's temperature down to 52. still a difference of 2,
        # which makes us not switch off the pump.
        if True:
            source_thermometer.set_temperature(52)
            poller.poll('source cools even more, still some diff')
            self.assertTrue(pump_switch.is_on())
            self.assertNotIn(sink, source.requesters())

        # sink at 50, source falls down to 49.9. negative difference
        # -> pump off.
        if True:
            source_thermometer.set_temperature(49.9)
            poller.poll('negative diff')
            self.assertFalse(pump_switch.is_on())
            self.assertNotIn(sink, source.requesters())

        # sink cools down to 33.1. pump on due to huge difference. no
        # request though because 33.1 is well between sink's
        # hysteresis.
        if True:
            sink_thermometer.set_temperature(33.1)
            poller.poll()
            self.assertTrue(pump_switch.is_on())
            self.assertNotIn(sink, source.requesters())

        # sink cools down to 32.9 -> request heating
        if True:
            sink_thermometer.set_temperature(32.9)
            poller.poll()
            self.assertTrue(pump_switch.is_on())
            self.assertIn(sink, source.requesters())

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportBasicTest))

# suite.addTest(TransportBasicTest("test__pump_on_off_simple"))
# suite.addTest(TransportPeeksProducerTest("test__producer_not_peeked_when_consumer_satisfied"))

# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
