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

def create_switch(name, description, chiplabel, offset, direction):
    if direction == DIRECTION_IN:
        gpiod_direction = gpiod.LINE_REQ_DIR_IN
    elif direction == DIRECTION_OUT:
        gpiod_direction = gpiod.LINE_REQ_DIR_OUT
    else: 
        assert False

    chip = _open_chips.get(chiplabel)
    if chip is None:
        chip = gpiod.Chip(chiplabel, gpiod.Chip.OPEN_BY_LABEL)
        _open_chips[chiplabel] = chip

    line = chip.get_line(offset)
    line.request(consumer='openheating:'+name, type=gpiod_direction)

    return GPIOSwitch(name=name, description=description, line=line)
