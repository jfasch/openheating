#!/usr/bin/python3

from openheating import logutil
from openheating.dbus import dbusutil

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus object lifecycle testing service (used during unittests)')
parser.add_argument('--stamp-directory')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

@dbusutil.lifecycle(startup='announce_started', shutdown='announce_stopped')
class TheObjectWhichIsLifecycled:
    dbus = '<node></node>'

    def __init__(self, stampdir):
        self.__stampdir = stampdir
    def announce_started(self):
        with open(self.__stampdir + '/started', 'w'):
            pass
    def announce_stopped(self):
        with open(self.__stampdir + '/stopped', 'w'):
            pass

dbusutil.run_server(
    loop=loop,
    bus=bus,
    busname=dbusutil.LIFECYCLETESTER_BUSNAME,
    objects=[('/', TheObjectWhichIsLifecycled(stampdir=args.stamp_directory))],
)
