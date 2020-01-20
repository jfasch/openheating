from .switch import Switch
from .error import HeatingError

import gpiod

import asyncio
from collections import deque


def input(name, description, chiplabel, offset):
    return switch(name=name, description=description, 
                  chiplabel=chiplabel, offset=offset, direction=DIRECTION_IN)

def output(name, description, chiplabel, offset):
    return switch(name=name, description=description, 
                  chiplabel=chiplabel, offset=offset, direction=DIRECTION_OUT)

def switch(chiplabel, offset, direction):
    if direction == DIRECTION_IN:
        gpiod_type = gpiod.LINE_REQ_DIR_IN
    elif direction == DIRECTION_OUT:
        gpiod_type = gpiod.LINE_REQ_DIR_OUT
    else: 
        assert False, '{} is not a valid direction'.format(direction)

    line = _get_chip(chiplabel).get_line(offset)

    # request line.

    # hmm. funny inconsistency with sysfs /sys/class/gpio
    # behaviour. with sysfs, I take a line ("echo NN > export") and it
    # is not ON immediately. I set it by doing "echo 1 > value".

    # here, with libgpiod, if I take a line (line.request()) without
    # specifying a default value, then it sets the line to 1 by
    # itself.

    # workaround: specify "default_val=False", knowing that
    # Line.request's docstring says that default_val is deprecated.
    try:
        consumer = 'openheating:'+name
        line.request(consumer=consumer, type=gpiod_type, default_val=False)
    except OSError as e:
        raise HeatingError('gpio: cannot request {}: {}'.format(consumer, str(e)))

    return _GPIOSwitch(line=line)

def pushbutton(chiplabel, offset, debounce_limit):
    line = _get_chip(chiplabel).get_line(offset)
    line.request(consumer='openheating:pushbutton@{}:{}'.format(chiplabel, offset), type=gpiod.LINE_REQ_EV_FALLING_EDGE)
    return _GPIOPushButton(line=line, debounce_limit=debounce_limit, 
                           loop=asyncio.get_event_loop())

# one uses a chip to retrieve a gpio handle. the chip must remain open
# to keep the handle valid, which is what this dictionary is used for.
_open_chips = {}
def _get_chip(chiplabel):
    chip = _open_chips.get(chiplabel)
    if chip is None:
        chip = gpiod.Chip(chiplabel, gpiod.Chip.OPEN_BY_LABEL)
        _open_chips[chiplabel] = chip
    return chip


DIRECTION_IN = 0
DIRECTION_OUT = 1

class _GPIOSwitch(Switch):
    def __init__(self, line):
        super().__init__()
        self.__line = line

    def set_state(self, state):
        self.__line.set_value(state and 1 or 0)

    def get_state(self):
        return (self.__line.get_value() == 1) and True or False

class _GPIOPushButton:
    def __init__(self, line, loop, debounce_limit):
        self.__line = line
        self.__debounce_limit = debounce_limit
        self.__loop = loop
        self.__debouncers = set()

        self.__loop.add_reader(line.event_get_fd(), self.__notify)

    class Debouncer:
        def __init__(self):
            self.first_event = asyncio.Future()
            self.counter = 0
            self.events = []
    
    async def state_changed(self):
        debouncer = self.Debouncer()
        self.__debouncers.add(debouncer)
        
        await debouncer.first_event

        # debounce in a loop
        while True:
            await asyncio.sleep(self.__debounce_limit)
            if debouncer.counter == 0:  # no more events within debounce_limit
                self.__debouncers.remove(debouncer)
                return debouncer.events
            else:   # continue debouncing
                debouncer.counter = 0

    def __notify(self):
        ev = self.__line.event_read()
        timestamp = ev.sec + ev.nsec/1000000000
        for debouncer in self.__debouncers:
            debouncer.events.append(timestamp)
            if debouncer.first_event.done():
                debouncer.counter += 1
            else:
                debouncer.first_event.set_result(None)
