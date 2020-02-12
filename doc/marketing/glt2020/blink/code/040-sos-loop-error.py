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

async def sos(led):
    for _ in range(3):
        led.on()
        await asyncio.sleep(0.2)
        led.off()
        await asyncio.sleep(0.2)

    for _ in range(3):
        led.on()
        await asyncio.sleep(0.7)
        led.off()
        await asyncio.sleep(0.7)

    for _ in range(3):
        led.on()
        await asyncio.sleep(0.2)
        led.off()
        await asyncio.sleep(0.2)

async def forever(coro):
    while True:
        await coro
        await asyncio.sleep(2)

loop = asyncio.get_event_loop()
loop.run_until_complete(forever(sos(light)))
