#!/usr/bin/python3

from openheating.base import pyconf
from openheating.panel.program import *

import sys
import re
import asyncio
import signal
import time


relays = pyconf.read_switches(open(sys.argv[1]).read())

interval = 20
prog = forever(
    *[sequence(debug('ON', relay.get_description()), on(relay), sleep(interval)) for relay in relays],
    *[sequence(debug('OFF', relay.get_description()), off(relay), sleep(interval)) for relay in relays],
)


# interval = 0.5
# prog = forever(
#     *[sequence(debug(relay.get_name(), relay.get_description()), on(relay), sleep(interval), off(relay), sleep(interval), ) for relay in relays],
# )

asyncio.get_event_loop().run_until_complete(launch(prog))

signal.pause()
