from .thinking import Thinker
from .sink import Sink
from .hysteresis import Hysteresis
from .oil_wood import OilWoodCombination
from .oil import OilCombo
from .passive_source import PassiveSource
from .transport import Transport

class JFControl(Thinker):
    def __init__(self,
                 th_essraum,
                 th_boiler_top,
                 th_ofen,
                 th_oil,
                 sw_pumpe_ww,
                 sw_pumpe_hk,
                 sw_oil_burn,
                 sw_wood_valve):

        self.__sink_ww = Sink(
            name='boiler', 
            thermometer=th_boiler_top, 
            temperature_range=Hysteresis(low=50, high=55),
        )

        self.__sink_room = Sink(
            name='room', 
            thermometer=th_essraum, 
            temperature_range=Hysteresis(low=20, high=21),
        )

        self.__source = OilWoodCombination(
            name='oil+wood',
            oil=OilCombo(
                name='oil',
                burn_switch=sw_oil_burn,
                thermometer=th_oil,
                heating_range=Hysteresis(50,70),
                minimum_temperature_range=Hysteresis(10,20),
                max_produced_temperature=90, # let's say
            ),
            wood=PassiveSource(
                name='wood', 
                thermometer=th_ofen,
                max_produced_temperature=50, # let's say
            ),
            valve_switch=sw_wood_valve,
            wood_warm=Hysteresis(30, 32),
            wood_hot=Hysteresis(40, 42),
        )

        self.__transport_ww = Transport(
            name='ww',
            source=self.__source, 
            sink=self.__sink_ww, 
            # adapt hysteresis to something more realistic
            diff_hysteresis=Hysteresis(low=5, high=10), 
            pump_switch=sw_pumpe_ww)

        self.__transport_hk = Transport(
            name='hk',
            source=self.__source, 
            sink=self.__sink_room, 
            # adapt hysteresis to something more realistic
            diff_hysteresis=Hysteresis(low=1, high=2), 
            pump_switch=sw_pumpe_hk)
        
    def register_thinking(self, brain):
        self.__sink_ww.register_thinking(brain)
        self.__sink_room.register_thinking(brain)
        self.__source.register_thinking(brain)
        self.__transport_ww.register_thinking(brain)
        self.__transport_hk.register_thinking(brain)
