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


parser = argparse.ArgumentParser(description='OpenHeating: crashtest dummy')
parser.add_argument(
    '--no-busname', action='store_true',
    help="don't register busname ({}), to see a timeout happen after startup".format(names.Bus.CRASHTESTDUMMY))
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.CRASHTESTDUMMY)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)


@node.Definition(interfaces=[])
class Crasher:
    def __init__(self):
        pass

if args.no_busname is True:
    busname = None
else:
    busname = names.Bus.CRASHTESTDUMMY

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=busname,
    objects=[('/', Crasher())],
)
