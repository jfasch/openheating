#!/usr/bin/python


import led
import asyncio


def program(fun):
    def creator(*args, **kwargs):
        def launch():
            # create a coroutine, readily wrapped in a asyncio Future
            return asyncio.ensure_future(fun(*args, **kwargs))
        return launch
    return creator

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
async def forever(*progs):
    while True:
        for p in progs:
            current = p()
            await current

@program
async def sleep(secs):
    await asyncio.sleep(secs)

led = led.LED_nohw()
prog = forever(sos(led), sleep(2))

loop = asyncio.get_event_loop()
loop.run_until_complete(prog())
