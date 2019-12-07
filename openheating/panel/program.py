from collections import namedtuple
import subprocess
import asyncio
import functools
import sys


LEDButton = namedtuple('LEDButton', ('led', 'button'))


def program(corofunc):
    # this is what you get when you write
    #   @program
    #   async def blah(a, b, c): ...

    # when called, it gives you a function create_coro() 
    def factory(*args, **kwargs):
        # create_coro(), when called, gives the caller the actual
        # coroutine to work with.
        def create_coro():
            return corofunc(*args, **kwargs)
        return create_coro
    return factory

def launch(prog):
    return asyncio.ensure_future(prog())

@program
async def blink(interval, led):
    state = saved_state = led.get_state()
    try:
        while True:
            state = not state
            led.set_state(state)
            await asyncio.sleep(interval)
    finally:
        led.set_state(saved_state)

@program
async def on(led):
    led.set_state(True)

@program
async def off(led):
    led.set_state(False)

@program
async def sequence(*progs):
    current = None
    try:
        for prog in progs:
            current = launch(prog)
            await current
    finally:
        if current:
            current.cancel()

@program
async def n_times(n, prog):
    current = None
    try:
        for _ in range(n):
            current = launch(prog)
            await current
    finally:
        if current:
            current.cancel()

@program
async def forever(*progs):
    current = None
    try:
        while True:
            for prog in progs:
                current = launch(prog)
                await current
    finally:
        if current: 
            current.cancel()

@program
async def all(*progs):
    'run progs in parallel and wail until all are done'
    task = asyncio.ensure_future(asyncio.gather(*[p() for p in progs]))
    try:
        await task
    except asyncio.CancelledError:
        task.cancel()

@program
async def any(*progs):
    tasks = [launch(prog) for prog in progs]
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()
    except asyncio.CancelledError:
        for task in tasks:
            task.cancel()

@program
async def sleep(secs):
    await asyncio.sleep(secs)

@program
async def debug(*args):
    print(*args, file=sys.stderr)

@program
async def wait_button(button):
    await button.state_changed()

@program
async def subprocess_shell(cmd):
    process = await asyncio.create_subprocess_shell(cmd)
    try:
        await process.wait()
    except asyncio.CancelledError:
        process.terminate()

@program
async def http_get(url):
    url += '?menu=false'
    prog = subprocess_shell('/usr/bin/chromium-browser --no-new-tab {}'.format(url))
    await prog()

@program
async def wake_display():
    prog = subprocess_shell('xset s reset')
    await prog()

def duration(delta, prog):
    return any(
        prog,
        sleep(delta),
    )
