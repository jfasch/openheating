#!/usr/bin/python3

from openheating import logutil
from openheating.dbus import dbusutil

from gi.repository import GLib
import pydbus

import signal
import argparse


parser = argparse.ArgumentParser(description='OpenHeating: Error handler/logger')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

def handle_error(*args):
    print(args)

bus.subscribe(
    iface=dbusutil.ERROREMITTER_IFACENAME,
    signal='error',
    signal_fired=handle_error)

dbusutil.graceful_termination(loop)

loop.run()
