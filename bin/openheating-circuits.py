#!/usr/bin/python3

from openheating.base import pyconf
from openheating.base import logutil
from openheating.dbus import dbusutil
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.circuit import Circuit_Server
from openheating.dbus.circuit_center import CircuitCenter_Server

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus circuit service')
parser.add_argument('--pyconfigfile', help='Circuit configuration file (python)')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

with open(args.pyconfigfile) as f:
    circuits = pyconf.read_circuits(f, bus)

objects = [
    ('/', CircuitCenter_Server(circuits=circuits))
]

for circuit in circuits:
    objects.append(('/circuits/'+circuit.get_name(), 
                    Circuit_Server(circuit=circuit)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.CIRCUITS,
    objects=objects,
)
