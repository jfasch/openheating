#!/usr/bin/python

import asyncio


class LED:
    def __init__(self):
        self.__state = False
    def on(self):
        self.__state = True
        print('on')
    def off(self):
        self.__state = False
        print('off')

light = LED()

async def blink(led, interval):
    while True:
        led.on()
        await asyncio.sleep(interval)
        led.off()
        await asyncio.sleep(interval)

loop = asyncio.get_event_loop()
loop.run_until_complete(blink(light, interval=0.5))
