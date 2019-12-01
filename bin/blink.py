#!/usr/bin/python3

from openheating.base import gpio

import time
import asyncio
import itertools


loop = asyncio.get_event_loop()

red_led = gpio.create_switch(
    name='red',
    description='Red LED',
    chiplabel='pinctrl-bcm2835',
    offset=21,
    direction=gpio.DIRECTION_OUT)

async def blink(switch, interval):
    state = False
    while True:
        state = not state
        switch.set_state(state)
        await asyncio.sleep(interval)

pushbutton = gpio.create_pushbutton(
    name='button',
    description='button',
    chiplabel='pinctrl-bcm2835',
    offset=20,
    loop=loop,
    debounce_limit=0.2)

async def part(loop, duration, func, *args):
    task = loop.create_task(func(*args))
    await asyncio.sleep(duration)
    task.cancel()

async def rotate():
    while True:
        await part(loop, 3, blink, red_led, 0.1)
        await part(loop, 3, blink, red_led, 0.4)
        await part(loop, 3, blink, red_led, 1)

loop.run_until_complete(rotate())
