#!/usr/bin/python

import asyncio


def program(fun):
    def creator(*args, **kwargs):
        def launch():
            return fun(*args, **kwargs)
        return launch
    return creator

class LED:
    def __init__(self, name, indent):
        self.__name = name
        self.__indent = indent
        self.__state = False
    def on(self):
        self.__state = True
        print(' '*self.__indent, self.__name, 'on')
    def off(self):
        self.__state = False
        print(' '*self.__indent, self.__name, 'off')

red = LED(name='red', indent=0)

@program
async def sos(led):
    for _ in range(3):
        led.on()
        await asyncio.sleep(0.1)
        led.off()
        await asyncio.sleep(0.1)

    for _ in range(3):
        led.on()
        await asyncio.sleep(0.5)
        led.off()
        await asyncio.sleep(0.5)

    for _ in range(3):
        led.on()
        await asyncio.sleep(0.1)
        led.off()
        await asyncio.sleep(0.1)

async def forever(prog):
    while True:
        current_coro = asyncio.ensure_future(prog())
        await current_coro

loop = asyncio.get_event_loop()

prog = forever(sos(red))

loop.run_until_complete(prog)
