#!/usr/bin/python3

from openheating.base import pyconf
from openheating.panel.program import *

import sys
import re
import asyncio
import signal
import time


relays = pyconf.read_switches(open(sys.argv[1]).read())

prog = forever(
    *[sequence(on(relay), sleep(0.2)) for relay in relays],
    sleep(0.5),
    *[sequence(off(relay), sleep(0.2)) for relay in relays],
    sleep(0.5),
)

asyncio.get_event_loop().run_until_complete(launch(prog))

signal.pause()
