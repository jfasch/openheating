#!/usr/bin/python

import led
import asyncio


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

led = led.LED_nohw()

loop = asyncio.get_event_loop()
loop.run_until_complete(sos(led))
