#!/usr/bin/python3

from openheating.dbus import dbusutil
from openheating.dbus.exception_tester import ExceptionTester_Server
from openheating import logutil

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: Exception testing service (used during unittests)')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

dbusutil.graceful_termination(loop)

bus.request_name(dbusutil.EXCEPTIONTESTER_BUSNAME)
bus.register_object('/', ExceptionTester_Server(), None)
loop.run()