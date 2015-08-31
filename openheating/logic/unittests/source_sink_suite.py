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
    def setUp(self):
        self.__source_thermometer = TestThermometer(initial_temperature=20)
        self.__source = _TestSource(name='source', thermometer=self.__source_thermometer)

        self.__sink_switch = TestSwitch(name='pump', initial_state=False)
        self.__sink_thermometer = TestThermometer(initial_temperature=20)
        self.__sink = Sink(name='sink', 
                           thermometer=self.__sink_thermometer, 
                           temperature_range=Hysteresis(23, 30),
                           diff_hysteresis=Hysteresis(1,2), 
                           pump_switch=self.__sink_switch)

        self.__source.add_sink(self.__sink)

        self.__brain = Brain([self.__source, self.__sink])

    def test__sink_rising(self):
        '''Sink below range, rises, and stops needing once above range.

        When between range, it continues to need because the
        temperature is rising - which is the entire point of the
        hysteresis thing I believe.

        '''

        # source 20, sink 20. sink needs (>23), source has 20 -> pump
        # off.
        if True:
            self.__source_thermometer.set_temperature(20)
            self.__sink_thermometer.set_temperature(20)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), False)
            self.assertEqual(self.__sink.test__get_need(), True)

        # source 60, sink 20. sink needs (>23), source has quite a lot
        # -> pump on.
        if True:
            self.__source_thermometer.set_temperature(60)
            self.__sink_thermometer.set_temperature(20)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), True)
            self.assertEqual(self.__sink.test__get_need(), True)

        # source 60, sink 23.2. sink still needs because was below
        # range in the previous step above, and is within range right
        # now. (rising, so to say)
        if True:
            self.__source_thermometer.set_temperature(60)
            self.__sink_thermometer.set_temperature(23.2)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), True)
            self.assertEqual(self.__sink.test__get_need(), True)

        # source 60, sink 30.1 (above range). sink does not need
        # anymore, but announces that it *could* take. sink still
        # takes (source has 60) because noone else needs.
        if True:
            self.__source_thermometer.set_temperature(60)
            self.__sink_thermometer.set_temperature(30.1)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), True)
            # sink does not need neither care about any need -> None
            self.assertEqual(self.__sink.test__get_need(), None)

    def test__sink_falling(self):
        '''Sink above range, falls, and does not need again once it is below
        range.

        When between range, it will not need because the
        temperature is falling - which is the entire point of the
        hysteresis thing I believe.

        '''
        self.fail()

    def test__diff(self):
        '''Source and sink must differ by a certain (configurable)
        amount/range of degrees (diff_hysteresis) - (1,2) here.

        '''

        # a difference of 0.1 does not switch on the pump.
        if True:
            self.__source_thermometer.set_temperature(25)
            self.__sink_thermometer.set_temperature(24.9)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), False)

        # 1.1 still does not switch on the pump. only when we cross
        # the 2 degrees upper bound it does.
        if True:
            self.__source_thermometer.set_temperature(25)
            self.__sink_thermometer.set_temperature(23.9)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), False)

        # 2.1 now *does* switch on the pump.
        if True:
            self.__source_thermometer.set_temperature(25)
            self.__sink_thermometer.set_temperature(22.9)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), True)

        # 1.5 *does not* switch off the pump (only below 1 - which is
        # the entire point of hysteresis)
        if True:
            self.__source_thermometer.set_temperature(25)
            self.__sink_thermometer.set_temperature(23.5)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), True)

        # 0.9 (right below) now does switch off the pump
        if True:
            self.__source_thermometer.set_temperature(25)
            self.__sink_thermometer.set_temperature(24.1)
            self.__brain.think()
            self.assertEqual(self.__sink_switch.get_state(), False)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(_SourceSinkSuite)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
