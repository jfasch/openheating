#!/usr/bin/python3

from openheating.dbus import cmdline
from openheating.dbus import error_emitter

from gi.repository import GLib
from pydbus.generic import signal

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: Error handler/logger')
cmdline.add_dbus_options(parser)
args = parser.parse_args()

class DummyForEmittingErrors:
    dbus = '<node>' + error_emitter.iface + '</node>'
    error = signal()

dummy = DummyForEmittingErrors()
bus = cmdline.bus(args)
bus.register_object('/', dummy, None)
dummy.error('fuck!')

bus.con.flush_sync()
