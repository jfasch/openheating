#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.plant.config_circuits import CircuitsConfig
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

logutil.configure_from_argparse(args, componentname=names.Bus.CIRCUITS)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

config = CircuitsConfig()
config.parse(args.config, bus=bus)

circuit_objects = [] # for center to know
path_n_objects = [] # [(path, object)], to publish

for name, description, circuit in config.get_circuits():
    cobj = Circuit_Server(name=name, description=description, circuit=circuit)
    circuit_objects.append(cobj)
    path_n_objects.append(('/circuits/'+name, cobj))

path_n_objects.append(('/', CircuitCenter_Server(objects=circuit_objects)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.CIRCUITS,
    objects=path_n_objects,
)
