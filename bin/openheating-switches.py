#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.plant.config import SwitchesConfig
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.switch import Switch_Server
from openheating.dbus.switch_center import SwitchCenter_Server

from gi.repository import GLib

import argparse
import os


parser = argparse.ArgumentParser(description='OpenHeating: DBus switch service')
parser.add_argument('--config', help='Configuration file')
parser.add_argument('--simulation-dir', metavar='DIR', 
                    help='Create "switch" files in DIR, and read/write states from/to there.')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.SWITCHES)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

if args.simulation_dir is not None:
    os.makedirs(args.simulation_dir, exist_ok=True)
config = SwitchesConfig(simulation_dir=args.simulation_dir)
config.parse(args.config, bus=bus)

objects = [
    ('/', SwitchCenter_Server(names=[name for name,_,_ in config.get_switches()]))
]

for name, description, switch in config.get_switches():
    objects.append(('/switches/'+name, 
                    Switch_Server(name=name, description=description, switch=switch)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.SWITCHES,
    objects=objects,
)
