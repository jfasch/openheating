#!/usr/bin/python


import asyncio


def program(fun):
    def creator(*args, **kwargs):
        def launch():
            return fun(*args, **kwargs)
        return launch
    return creator

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

@program
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

@program
async def forever(prog):
    while True:
        current = asyncio.ensure_future(prog())
        await current

prog = sos(light)

loop = asyncio.get_event_loop()
loop.run_until_complete(prog())
