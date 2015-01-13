from openheating.testutils.switch import TestSwitch
from openheating.testutils.thermometer import TestThermometer

from openheating.thinking import Brain
from openheating.sink import Sink
from openheating.passive_source import PassiveSource
from openheating.hysteresis import Hysteresis
from openheating.transport import Transport

import unittest
import logging

class TransportBasicTest(unittest.TestCase):
    def test__basic(self):
        brain = Brain()
        
        sink_thermometer = TestThermometer(initial_temperature=20)
        sink = Sink(name='my-sink', thermometer=sink_thermometer,
                    hysteresis=Hysteresis(33, 47))
        brain.add(sink)

        source_thermometer = TestThermometer(initial_temperature=80)
        source = PassiveSource(name='my-source', thermometer=source_thermometer)

        pump_switch = TestSwitch(name='pump', initial_state=TestSwitch.OPEN)
        transport = Transport(name='my-transport', source=source, sink=sink,
                              diff_hysteresis=Hysteresis(0, 5),
                              pump_switch=pump_switch)
        brain.add(transport)

        # pump is off initially. switched on after first move, due to
        # difference of 60 degrees. sink is far below its desired
        # temperature, so it explicitly requests heating
        if True:
            self.assertTrue(pump_switch.is_open())
            brain.think('initial, diff is huge, request')
            self.assertTrue(pump_switch.is_closed())
            self.assertIn(sink, source.requesters())

        # sink reaches its desired temperature. pump is kept running
        # nonetheless - it's the temperature difference which
        # matters. no heating explicitly requested anymore though.
        if True:
            sink_thermometer.set_temperature(50)
            brain.think('sink satisfied, diff still there')
            self.assertTrue(pump_switch.is_closed())
            self.assertNotIn(sink, source.requesters())

        # source's temperature falls to 55.1. this makes a temperature
        # difference of 5.1. threshold is 5, so pump is kept running.
        if True:
            source_thermometer.set_temperature(55.1)
            brain.think('source cools, still some diff')
            self.assertTrue(pump_switch.is_closed())
            self.assertNotIn(sink, source.requesters())
            
        # source's temperature down to 52. still a difference of 2,
        # which makes us not switch off the pump.
        if True:
            source_thermometer.set_temperature(52)
            brain.think('source cools even more, still some diff')
            self.assertTrue(pump_switch.is_closed())
            self.assertNotIn(sink, source.requesters())

        # sink at 50, source falls down to 49.9. negative difference
        # -> pump off.
        if True:
            source_thermometer.set_temperature(49.9)
            brain.think('negative diff')
            self.assertTrue(pump_switch.is_open())
            self.assertNotIn(sink, source.requesters())

        # sink cools down to 33.1. pump on due to huge difference. no
        # request though because 33.1 is well between sink's
        # hysteresis.
        if True:
            sink_thermometer.set_temperature(33.1)
            brain.think()
            self.assertTrue(pump_switch.is_closed())
            self.assertNotIn(sink, source.requesters())

        # sink cools down to 32.9 -> request heating
        if True:
            sink_thermometer.set_temperature(32.9)
            brain.think()
            self.assertTrue(pump_switch.is_closed())
            self.assertIn(sink, source.requesters())

    def test__2sinks(self):
        # Two sinks, one source. if there's temperature difference in
        # both transports, there has to be some coordination between
        # those.

        # * requested: heat flows only to those who explictly
        #   requested. the others remain off.

        # * nothing requested: heat flows into all sinks where there
        #   is difference. we don't want to leave heat in the source,
        #   it would be wasted there.

        brain = Brain()
        
        source_thermometer = TestThermometer(initial_temperature=80)
        source = PassiveSource(name='my-source', thermometer=source_thermometer)

        sink1_thermometer = TestThermometer(initial_temperature=20)
        sink1 = Sink(name='my-sink-1', thermometer=sink1_thermometer,
                     hysteresis=Hysteresis(33, 47))
        brain.add(sink1)

        sink2_thermometer = TestThermometer(initial_temperature=20)
        sink2 = Sink(name='my-sink-2', thermometer=sink2_thermometer,
                    hysteresis=Hysteresis(33, 47))
        brain.add(sink2)

        pump1_switch = TestSwitch(name='pump1', initial_state=TestSwitch.OPEN)
        transport1 = Transport(name='my-transport-1', source=source, sink=sink1,
                                diff_hysteresis=Hysteresis(0, 5),
                                pump_switch=pump1_switch)
        brain.add(transport1)

        pump2_switch = TestSwitch(name='pump2', initial_state=TestSwitch.OPEN)
        transport2 = Transport(name='my-transport-2', source=source, sink=sink2,
                               diff_hysteresis=Hysteresis(0, 5),
                               pump_switch=pump2_switch)
        brain.add(transport2)

        # both sinks request some heat.
        if True:
            brain.think('both sinks request')
            self.assertIn(sink1, source.requesters())
            self.assertIn(sink2, source.requesters())

        # pumps on (done in a second poll round since poll sequence is
        # not deterministic)
        if True:
            brain.think('pumps on')
            self.assertTrue(pump1_switch.is_closed())
            self.assertTrue(pump2_switch.is_closed())

        # both sinks reach their temperature -> release, both pumps
        # remain on (because temperatures differ enough)
        if True:
            sink1_thermometer.set_temperature(50)
            sink2_thermometer.set_temperature(50)
            brain.think('both sinks release, pumps still on')
            self.assertEqual(len(source.requesters()), 0)
            self.assertNotIn(sink1, source.requesters())
            self.assertNotIn(sink2, source.requesters())
            self.assertTrue(pump1_switch.is_closed())
            self.assertTrue(pump2_switch.is_closed())

        # sink1 cools down -> request. sink1 is the only requester, so
        # only pump1 must be running, and pump2 must be off.
        if True:
            sink1_thermometer.set_temperature(0)
            brain.think('sink1 cools down')
            self.assertEqual(len(source.requesters()), 1)
            self.assertIn(sink1, source.requesters())
            self.assertTrue(pump1_switch.is_closed())
            self.assertTrue(pump2_switch.is_open())

        # sink1 heats up again, releases. both pumps running again.
        if True:
            sink1_thermometer.set_temperature(50)
            brain.think('sink1 releases')
            self.assertEqual(len(source.requesters()), 0)
            self.assertTrue(pump1_switch.is_closed())
            self.assertTrue(pump2_switch.is_closed())

        # source cools down -> both pumps off
        if True:
            source_thermometer.set_temperature(0)
            brain.think('source cool, both pumps off')
            self.assertTrue(pump1_switch.is_open())
            self.assertTrue(pump2_switch.is_open())
            

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TransportBasicTest))

#suite.addTest(TransportBasicTest("test__2sinks"))

#logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
