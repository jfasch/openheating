from . import gpio

from ..switch import Switch

class GPIOSwitch(Switch):
    def __init__(self, number):
        self.__gpio = gpio.create(number)
        self.__gpio.set_direction(gpio.OUT)

    def set_state(self, value):
        assert type(value) is bool
        self.__gpio.set_value(value)
            
    def get_state(self):
        return self.__gpio.get_value() and True or False
