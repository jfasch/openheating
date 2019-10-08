#!/usr/bin/python3

from openheating.dbus import dbusutil

from gi.repository import GLib
from pydbus.generic import signal

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: Error handler/logger')
dbusutil.argparse_add_bus(parser)
args = parser.parse_args()

bus = dbusutil.bus_from_argparse(args)

# register dummy object on unnamed connection, for the sole purpose of
# emitting the error signal from its only interface.
class DummyForEmittingErrors:
    error = signal()
dbusutil.NodeDefinition(interfaces=(dbusutil.ERROREMITTER_IFACEXML,))\
.apply_to(DummyForEmittingErrors)

dummy = DummyForEmittingErrors()
bus.register_object('/', dummy, None)

dummy.error('fuck!')
bus.con.flush_sync()
