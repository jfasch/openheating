from .gpio import OUT as gpio_out

from ..switch import Switch

class GPIOSwitch(Switch):
    def __init__(self, gpio):
        self.__gpio = gpio
        self.__gpio.set_direction(gpio_out)

    def set_state(self, value):
        assert type(value) is bool
        self.__gpio.set_value(value)
            
    def get_state(self):
        return self.__gpio.get_value() and True or False
