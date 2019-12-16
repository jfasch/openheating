#!/usr/bin/python3

from openheating.base import pyconf
from openheating.panel.program import *

import sys
import re
import asyncio
import signal


board1 = [None] * 8
board2 = [None] * 8

for s in pyconf.read_switches(open(sys.argv[1]).read()):
    name = s.get_name()
    match = re.search(r'^Relay(\d)_(\d)$', name)
    assert match

    if int(match.group(1)) == 1:
        board1[int(match.group(2))-1] = s
    elif int(match.group(1)) == 2:
        board2[int(match.group(2))-1] = s


prog = sequence(
    sequence(
        *[sequence(on(board1[i]),sleep(0.2)) for i in range(8)]
    ),
    # sequence(
    #     *[sequence(on(board2[i]),sleep(0.2)) for i in range(8)]
    # ),
)

prog = forever(
    *[sequence(on(board1[i]), sleep(0.2)) for i in range(8)],
    sleep(0.5),
    *[sequence(off(board1[i]), sleep(0.2)) for i in range(8)],
    sleep(0.5),
)

asyncio.get_event_loop().run_until_complete(launch(prog))

signal.pause()
