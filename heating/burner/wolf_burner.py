from ..control.switch import Switch
from ..control.producer import Producer
from ..control.thermometer import Thermometer

class WolfBurner(Producer):
    def __init__(self,
                 inhibit_switch,
                 burn_switch,
                 thermometer):
        assert isinstance(inhibit_switch, Switch)
        assert isinstance(burn_switch, Switch)
        assert isinstance(thermometer, Thermometer)
        
        self.__inhibit_switch = inhibit_switch
        self.__burn_switch = burn_switch
        self.__thermometer = thermometer

    def temperature(self):
        return self.__thermometer.temperature()

    def acquire(self):
        self.__burn_switch.on()

    def release(self):
        self.__burn_switch.off()
        
