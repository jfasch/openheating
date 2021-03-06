#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.dbus import names
from openheating.dbus import lifecycle

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus managed object testing service (used during unittests)')
parser.add_argument('--stamp-directory')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.MANAGEDOBJECTTESTER)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

@lifecycle.managed(startup='announce_started', shutdown='announce_stopped')
class TheObjectWhichIsManaged:
    dbus = '<node></node>'

    def __init__(self, stampdir):
        self.__stampdir = stampdir
    def announce_started(self):
        with open(self.__stampdir + '/started', 'w'):
            pass
    def announce_stopped(self):
        with open(self.__stampdir + '/stopped', 'w'):
            pass

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.MANAGEDOBJECTTESTER,
    objects=[('/', TheObjectWhichIsManaged(stampdir=args.stamp_directory))],
)
