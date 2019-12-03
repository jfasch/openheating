#!/usr/bin/python3

from openheating.base import gpio
from openheating.base import panelutil

import asyncio
import itertools


loop = asyncio.get_event_loop()

red = panelutil.LEDButton(
    gpio.create_switch(
        name='red_led',
        description='Red LED',
        chiplabel='pinctrl-bcm2835',
        offset=21,
        direction=gpio.DIRECTION_OUT),
    gpio.create_pushbutton(
        name='red_button',
        description='Red Button',
        chiplabel='pinctrl-bcm2835',
        offset=20,
        loop=loop,
        debounce_limit=0.2)
)
yellow = panelutil.LEDButton(
    gpio.create_switch(
        name='yellow_led',
        description='Yellow LED',
        chiplabel='pinctrl-bcm2835',
        offset=12,
        direction=gpio.DIRECTION_OUT),
    gpio.create_pushbutton(
        name='yellow_button',
        description='Yellow Button',
        chiplabel='pinctrl-bcm2835',
        offset=7,
        loop=loop,
        debounce_limit=0.2)
)
green = panelutil.LEDButton(
    gpio.create_switch(
        name='greem_led',
        description='Green LED',
        chiplabel='pinctrl-bcm2835',
        offset=24,
        direction=gpio.DIRECTION_OUT),
    gpio.create_pushbutton(
        name='green_button',
        description='Green Button',
        chiplabel='pinctrl-bcm2835',
        offset=23,
        loop=loop,
        debounce_limit=0.2)
)

prog__red_button_http2thermometers = asyncio.gather(
    panelutil.button_runs_subprocess(
        button=red.button,
        cmd=['/usr/bin/chromium-browser', '--no-new-tab', 'http://192.168.1.30:5000/thermometers']),
    panelutil.button_stops(
        button=yellow.button,
        coro=panelutil.iterate_frequencies(
            led=yellow.led,
            interval=3,
            frequencies=itertools.cycle((0.1, 0.5, 1))),
        and_then=panelutil.blink(0.05, led=yellow.led)),
    panelutil.button_iterates_frequencies(
        ledbutton=green,
        frequencies=itertools.cycle((0.1, 0.5, 1))),
)


loop.run_until_complete(prog__red_button_http2thermometers)
