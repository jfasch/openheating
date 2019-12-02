from collections import namedtuple
import asyncio


LEDButton = namedtuple('LEDButton', ('led', 'button'))

async def blink(interval, led):
    try:
        state = True
        while True:
            led.set_state(state)
            await asyncio.sleep(interval)
            state = not state
    finally:
        led.set_state(False)

async def on(led):
    led.set_state(True)

async def off(led):
    led.set_state(False)

async def duration(duration, coro):
    task = asyncio.ensure_future(coro)
    try:
        await asyncio.sleep(duration)
    finally:
        task.cancel()

async def sequence(*coroutines):
    for coro in coroutines:
        await coro

async def iterate_frequencies(led, interval, frequencies):
    for f in frequencies:
        await duration(interval, blink(f, led))

async def button_stops(button, coro, and_then=None):
    task = asyncio.ensure_future(coro)
    try:
        await button.state_changed()
    finally:
        task.cancel()

    if and_then:
        await button.state_changed()
        task = asyncio.ensure_future(and_then)
        try:
            await task
        finally:
            task.cancel()

async def button_iterates_frequencies(combo, frequencies):
    for f in frequencies:
        task = asyncio.ensure_future(blink(f, combo.led))
        try:
            await combo.button.state_changed()
        except CancelledError:
            break
        finally:
            task.cancel()

