#!/usr/bin/python

import asyncio


class LED:
    def __init__(self, color, indent):
        self.__color = color
        self.__indent = indent
        self.__state = False
    def on(self):
        self.__state = True
        print(' '*self.__indent, self.__color, 'on')
    def off(self):
        self.__state = False
        print(' '*self.__indent, self.__color, 'off')

green = LED(color='green', indent=0)
yellow = LED(color='yellow', indent=20)
red = LED(color='red', indent=40)

async def blink(led, interval):
    while True:
        led.on()
        await asyncio.sleep(interval)
        led.off()
        await asyncio.sleep(interval)

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(blink(led=green, interval=0.3),
                   blink(led=yellow, interval=0.5),
                   blink(led=red, interval=1),
    ))
