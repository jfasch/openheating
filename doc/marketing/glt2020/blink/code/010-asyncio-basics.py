#!/usr/bin/python

import led
import asyncio


async def blink(led, interval):
    while True:
        led.on()
        await asyncio.sleep(interval)
        led.off()
        await asyncio.sleep(interval)

led = led.LED_nohw()
loop = asyncio.get_event_loop()
loop.run_until_complete(blink(led, interval=0.5))
