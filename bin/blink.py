#!/usr/bin/python3

from openheating.base import gpio
from openheating.panel.program import *
from openheating.panel.cli import CLI

import asyncio
import sys
import argparse


parser = argparse.ArgumentParser('blinking weirdly')
parser.add_argument('--simulation', action='store_true', help='dont use real buttons')
parser.add_argument('programs', nargs='*', help='names of programs to launch')
args = parser.parse_args()


loop = asyncio.get_event_loop()

if args.simulation:
    green = yellow = red = LEDButton(None, None)
else:
    red = LEDButton(
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
    yellow = LEDButton(
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
    green = LEDButton(
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


def open_url(ledbutton, url):
    return forever(
        any(
            blink(1, ledbutton.led),
            wait_button(ledbutton.button),
        ),
        any(
            blink(0.1, ledbutton.led),
            sequence(
                wake_display(),
                http_get(url),
            ),
        ),
    )

programs = {
    'simple-blink-green': blink(1, green.led),
    'simple-blink-yellow': blink(1, yellow.led),
    'simple-blink-red': blink(1, red.led),
    'three-stages-blinking': forever(any(sleep(3), blink(0.2, green.led)),
                                     any(sleep(3), blink(0.2, yellow.led)),
                                     any(sleep(3), blink(0.2, red.led))),
    'parallel-blink-forever': all(
        blink(0.1, green.led),
        blink(0.2, yellow.led),
        blink(0.3, red.led),
    ),
    'parallel-blink-five-seconds': any(
        blink(0.1, green.led),
        blink(0.2, yellow.led),
        blink(0.3, red.led),
        sleep(5),
    ),
        
    'button-navigation': all(
        open_url(green, 'http://192.168.1.30:5000/'),
        open_url(yellow, 'http://192.168.1.30:5000/thermometers'),
        open_url(red, 'http://192.168.1.30:5000/errors'),
    ),

    'weird': forever(
        any(
            forever(
                debug('1'),
                sleep(0.2),
            ),
            sleep(1),
        ),
        debug('pause'),
        sleep(1),
    ),
}

async def cli():
    async for line in linereader(sys.stdin):
        print(line)

if len(args.programs):
    coro = launch(all(*[programs[pname] for pname in args.programs]))
else:
    coro = CLI(programs).run()

loop.run_until_complete(coro)
