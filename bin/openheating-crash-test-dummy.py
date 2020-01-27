#!/usr/bin/python3

from openheating.plant import dbusutil
from openheating.plant import logutil
from openheating.dbus import names
from openheating.dbus import node
from openheating.dbus import interface_repo
from openheating.dbus import lifecycle

from gi.repository import GLib

import argparse
import sys
import signal


parser = argparse.ArgumentParser(description='OpenHeating: crashtest dummy')
parser.add_argument(
    '--no-busname', action='store_true',
    help="don't register busname ({}), to see a timeout happen after startup".format(names.Bus.CRASHTESTDUMMY))
parser.add_argument(
    '--crash-in-operation-after-nsecs', type=int, metavar='N',
    help="crash in operation after N seconds")
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.CRASHTESTDUMMY)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

if args.no_busname is True:
    busname = None
else:
    busname = names.Bus.CRASHTESTDUMMY

if args.crash_in_operation_after_nsecs is not None:
    # arrange for SIGALRM to be sent after n secs. exit in the
    # handler.
    signal.signal(signal.SIGALRM, lambda _,__: sys.exit(1))
    signal.alarm(args.crash_in_operation_after_nsecs)

@node.Definition(interfaces=[])
class Crasher:
    def __init__(self):
        pass

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=busname,
    objects=[('/', Crasher())],
)
