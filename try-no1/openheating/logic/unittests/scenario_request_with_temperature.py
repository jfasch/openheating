from openheating.testutils.test_switch import TestSwitch
from openheating.testutils.test_thermometer import TestThermometer

from openheating.logic.brain import Brain
from openheating.logic.sink import Sink
from openheating.logic.passive_source import PassiveSource
from openheating.logic.hysteresis import Hysteresis
from openheating.logic.transport import Transport

import logging
import unittest


class ComplicatedScenarioTests(unittest.TestCase):
    '''boiler (a hot water buffer) has 50 degrees, but wants 60. boiler
    requests.

    room has 25 which is enough. room does not request.

    wood (oven) can never do what boiler requests. (wood's
    temperatures don't heat up at 60, at least not in my house.)


    error scenario discovered (and the reason for this test): 

    * boiler requests, room not. 

    * wood heats up to 40. room's transport won't switch on its
      pump - boiler is a requester and thus it should be favored.

    EFFECT: both pumps remain off: boiler has 50 and wood has
    40. room gave up in favor of requester.

    SOLUTION: do not only request blindly, but rather request a
    _temperature_. sources can then limit the temperature that can
    be requested, and simply deny the request.

    '''

    def test__2sinks__one_locks_out_other__source_explodes(self):
        # setup
        if True:
            wood_thermometer = TestThermometer(initial_temperature=40)
            wood = PassiveSource(name='wood', thermometer=wood_thermometer, max_produced_temperature=40)

            boiler_thermometer = TestThermometer(initial_temperature=50)
            boiler = Sink(name='boiler', thermometer=boiler_thermometer,
                          temperature_range=Hysteresis(58,62))

            room_thermometer = TestThermometer(initial_temperature=25)
            room = Sink(name='room', thermometer=room_thermometer,
                        temperature_range=Hysteresis(22, 23))

            boiler_pump_switch = TestSwitch(name='boiler-pump-switch', initial_state=False)
            boiler_transport = Transport(name='boiler-transport', source=wood, sink=boiler,
                                         diff_hysteresis=Hysteresis(0, 1),
                                         pump_switch=boiler_pump_switch)

            room_pump_switch = TestSwitch(name='room-pump-switch', initial_state=False)
            room_transport = Transport(name='room-transport', source=wood, sink=room,
                                       diff_hysteresis=Hysteresis(0, 1),
                                       pump_switch=room_pump_switch)

            brain = Brain([wood, boiler, room, boiler_transport, room_transport])

        brain.think('')

        self.assertTrue(boiler_pump_switch.is_open())
        self.assertTrue(room_pump_switch.is_closed())


suite = unittest.defaultTestLoader.loadTestsFromTestCase(ComplicatedScenarioTests)

#suite.addTest(TransportBasicTest("test__2sinks"))
#logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
