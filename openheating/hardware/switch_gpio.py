from .gpio import OUT as gpio_out

from ..switch import Switch

class GPIOSwitch(Switch):
    def __init__(self, gpio):
        self.__gpio = gpio
        self.__gpio.set_direction(gpio_out)

    def set_state(self, value):
        if value == self.OPEN:
            self.__gpio.set_value(False)
        elif value == self.CLOSED:
            self.__gpio.set_value(True)
        else:
            assert False, value
            
    def get_state(self):
        if self.__gpio.get_value():
            return self.CLOSED
        else:
            return self.OPEN
