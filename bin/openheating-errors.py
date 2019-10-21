#!/usr/bin/python3

from openheating import logutil
from openheating.dbus import dbusutil
from openheating.dbus.util import lifecycle
from openheating.dbus.errors import Errors_Server

from gi.repository import GLib
import pydbus

import signal
import argparse
import sys


parser = argparse.ArgumentParser(description='OpenHeating: Error handler/logger')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

errors = Errors_Server()

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=dbusutil.ERRORS_BUSNAME,
    objects=[('/', errors)],
    signals=[(dbusutil.SignalMatch(interface=dbusutil.ERROREMITTER_IFACENAME, name='error'), errors.handle_error)],
)
