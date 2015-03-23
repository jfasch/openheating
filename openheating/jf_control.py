from .thinking import Thinker
from .sink import Sink
from .hysteresis import Hysteresis
from .oil_wood import OilWoodCombination
from .oil import OilCombo
from .passive_source import PassiveSource
from .transport import Transport

class JFControl(Thinker):
    def __init__(self,
                 switch_center,
                 thermometer_center):

        self.__th_essraum = thermometer_center.get_thermometer('essraum')
        self.__th_boiler_top = thermometer_center.get_thermometer('boiler-top')
        self.__th_ofen = thermometer_center.get_thermometer('ofen')
        self.__th_oil = thermometer_center.get_thermometer('oel-puffer')
        self.__sw_pumpe_ww = switch_center.get_switch('pumpe-ww')
        self.__sw_pumpe_hk = switch_center.get_switch('pumpe-hk')
        self.__sw_oil_burn = switch_center.get_switch('oel-burn')
        self.__sw_wood_valve = switch_center.get_switch('wood-valve')

        self.__sink_ww = Sink(
            name='boiler', 
            thermometer=self.__th_boiler_top, 
            temperature_range=Hysteresis(low=50, high=55),
        )

        self.__sink_room = Sink(
            name='room', 
            thermometer=self.__th_essraum, 
            temperature_range=Hysteresis(low=20, high=21),
        )

        self.__source = OilWoodCombination(
            name='oil+wood',
            oil=OilCombo(
                name='oil',
                burn_switch=self.__sw_oil_burn,
                thermometer=self.__th_oil,
                heating_range=Hysteresis(50,70),
                minimum_temperature_range=Hysteresis(10,20),
                max_produced_temperature=90, # let's say
            ),
            wood=PassiveSource(
                name='wood', 
                thermometer=self.__th_ofen,
                max_produced_temperature=50, # let's say
            ),
            valve_switch=self.__sw_wood_valve,
            wood_warm=Hysteresis(30, 32),
            wood_hot=Hysteresis(40, 42),
        )

        self.__transport_ww = Transport(
            name='ww',
            source=self.__source, 
            sink=self.__sink_ww, 
            # adapt hysteresis to something more realistic
            diff_hysteresis=Hysteresis(low=5, high=10), 
            pump_switch=self.__sw_pumpe_ww)

        self.__transport_hk = Transport(
            name='hk',
            source=self.__source, 
            sink=self.__sink_room, 
            # adapt hysteresis to something more realistic
            diff_hysteresis=Hysteresis(low=1, high=2), 
            pump_switch=self.__sw_pumpe_hk)
        
    def register_thinking(self, brain):
        self.__sink_ww.register_thinking(brain)
        self.__sink_room.register_thinking(brain)
        self.__source.register_thinking(brain)
        self.__transport_ww.register_thinking(brain)
        self.__transport_hk.register_thinking(brain)
