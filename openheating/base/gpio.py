from .switch import Switch

import gpiod

# one uses a chip to retrieve a gpio handle. the chip must remain open
# to keep the handle valid, which is why this dictionary is there.
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
    if direction == DIRECTION_IN:
        gpiod_direction = gpiod.LINE_REQ_DIR_IN
    elif direction == DIRECTION_OUT:
        gpiod_direction = gpiod.LINE_REQ_DIR_OUT
    else: 
        assert False

    if dummy:
        return DummyGPIOSwitch(name, description, direction)

    chip = _open_chips.get(chiplabel)
    if chip is None:
        chip = gpiod.Chip(chiplabel, gpiod.Chip.OPEN_BY_LABEL)
        _open_chips[chiplabel] = chip

    line = chip.get_line(offset)
    line.request(consumer='openheating:'+name, type=gpiod_direction)

    return GPIOSwitch(name=name, description=description, line=line)
