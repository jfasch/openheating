#!/usr/bin/python3

from openheating.base import logutil
from openheating.dbus.config import CircuitsConfig
from openheating.dbus import dbusutil
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.circuit import Circuit_Server
from openheating.dbus.circuit_center import CircuitCenter_Server

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus circuit service')
parser.add_argument('--config', help='Configuration file')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

config = CircuitsConfig()
config.parse(args.config, bus=bus)

objects = [
    ('/', CircuitCenter_Server(circuits=config.get_circuits()))
]

for circuit in config.get_circuits():
    objects.append(('/circuits/'+circuit.get_name(), 
                    Circuit_Server(circuit=circuit)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.CIRCUITS,
    objects=objects,
)
