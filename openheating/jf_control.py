from .thinker import Thinker
from .sink import Sink
from .hysteresis import Hysteresis
from .oil_wood import OilWoodCombination
from .oil import OilCombo
from .passive_source import PassiveSource
from .transport import Transport
from .thermometer_center import ThermometerCenterThermometer
from .switch_center import SwitchCenterSwitch


class JFControl(Thinker):
    def __init__(self,
                 switch_center,
                 thermometer_center,
                 
                 th_room,
                 th_water,
                 th_wood,
                 th_oil,
                 sw_water,
                 sw_room,
                 sw_oil,
                 sw_wood_valve):

        self.__sink_ww = Sink(
            name = 'boiler', 
            thermometer = ThermometerCenterThermometer(thermometer_center, th_water), 
            temperature_range = Hysteresis(low=50, high=55),
        )

        self.__sink_room = Sink(
            name = 'room', 
            thermometer = ThermometerCenterThermometer(thermometer_center, th_room),
            temperature_range = Hysteresis(low=20, high=21),
        )

        self.__source = OilWoodCombination(
            name = 'oil+wood',
            oil = OilCombo(
                name = 'oil',
                burn_switch = SwitchCenterSwitch(switch_center, sw_oil),
                thermometer = ThermometerCenterThermometer(thermometer_center, th_oil),
                heating_range = Hysteresis(50,70),
                minimum_temperature_range = Hysteresis(10,20),
                max_produced_temperature = 90, # let's say
            ),
            wood=PassiveSource(
                name='wood', 
                thermometer = ThermometerCenterThermometer(thermometer_center, th_wood),
                max_produced_temperature=50, # let's say
            ),
            valve_switch = SwitchCenterSwitch(switch_center, sw_wood_valve),
            wood_warm=Hysteresis(30, 32),
            wood_hot=Hysteresis(40, 42),
        )

        self.__transport_ww = Transport(
            name='ww',
            source=self.__source, 
            sink=self.__sink_ww, 
            # adapt hysteresis to something more realistic
            diff_hysteresis=Hysteresis(low=5, high=10), 
            pump_switch=SwitchCenterSwitch(switch_center, sw_water))

        self.__transport_hk = Transport(
            name='hk',
            source=self.__source, 
            sink=self.__sink_room, 
            # adapt hysteresis to something more realistic
            diff_hysteresis=Hysteresis(low=1, high=2), 
            pump_switch=SwitchCenterSwitch(switch_center, sw_room))
        
    def register_thinking(self, brain):
        self.__sink_ww.register_thinking(brain)
        self.__sink_room.register_thinking(brain)
        self.__source.register_thinking(brain)
        self.__transport_ww.register_thinking(brain)
        self.__transport_hk.register_thinking(brain)
