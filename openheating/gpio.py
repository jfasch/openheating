from switch import Switch

import gpiod


_open_chips = {}

DIRECTION_IN = 0
DIRECTION_OUT = 1

class GPIOSwitch(Switch):
    def __init__(self, name, description, line):
        super().__init__(name, description)
        self.line = line

    def set_state(self, state):
        self.line.set_value(state and 1 or 0)

    def get_state(self):
        return (self.line.get_value() == 1) and True or False

class DummyGPIOSwitch(Switch):
    def __init__(self, name, description, direction):
        super().__init__(name, description)
        self.direction = direction
        self.state = False

    def set_state(self, state):
        if self.direction == _DIRECTION_IN:
            raise HeatingError('cannot set when direction is "in"')
        self.state = value

    def get_state(self):
        return self.state

def create_switch(name, description, chiplabel, offset, direction, dummy=False):
    if dummy:
        return DummyGPIOSwitch(name, description, direction)

    chip = _open_chips.get(chiplabel)
    if chip is None:
        chip = gpiod.Chip(chiplabel, gpiod.Chip.OPEN_BY_LABEL)
        _open_chips[chiplabel] = chip
    return GPIOSwitch(name=name, description=description, line=chip.get_line(offset))
