#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.dbus import node
from openheating.dbus import names
from openheating.dbus import interface_repo
from openheating.dbus import lifecycle
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

logutil.configure_from_argparse(args, componentname=names.Bus.ERRORS)
bus = dbusutil.bus_from_argparse(args)

errors = Errors_Server()

lifecycle.run_server(
    loop=GLib.MainLoop(),
    bus=bus,
    busname=names.Bus.ERRORS,
    objects=[('/', errors)],
    signals=[(node.SignalMatch(interface=interface_repo.ERROREMITTER, name='error'),
              errors.handle_error)],
)
