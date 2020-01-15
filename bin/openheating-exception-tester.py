#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.dbus import lifecycle
from openheating.dbus import names
from openheating.dbus.exception_tester import ExceptionTester_Server

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: Exception testing service (used during unittests)')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.EXCEPTIONTESTER,
    objects=[('/', ExceptionTester_Server())],
)
