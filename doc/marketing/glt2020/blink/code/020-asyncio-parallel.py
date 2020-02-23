#!/usr/bin/python

import led
import asyncio


async def blink(led, interval):
    while True:
        led.on()
        await asyncio.sleep(interval)
        led.off()
        await asyncio.sleep(interval)

green = led.LED_nohw(color='green', indent=0)
yellow = led.LED_nohw(color='yellow', indent=20)
red = led.LED_nohw(color='red', indent=40)

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(blink(led=green, interval=0.1),
                   blink(led=yellow, interval=1),
                   blink(led=red, interval=5),
    ))
