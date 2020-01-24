#!/usr/bin/python3

from openheating.plant import dbusutil
from openheating.plant import logutil
from openheating.dbus import names
from openheating.dbus import node
from openheating.dbus import interface_repo
from openheating.dbus import lifecycle

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: poll cycle witness (for testing only)')
parser.add_argument('--witness')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.POLLWITNESS)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

assert args.witness is not None

@node.Definition(interfaces=interface_repo.get(interface_repo.POLLABLE))
class PollWitness:
    def __init__(self, witness):
        self.__witness = witness
    def poll(self, timestamp):
        with open(self.__witness, 'w') as f:
            f.write(str(timestamp))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.POLLWITNESS,
    objects=[('/', PollWitness(witness=args.witness))],
)
