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
parser.add_argument('--simulated-switches-dir', metavar='DIR', 
                    help='Create "switch" files in DIR, and read/write states from/to there. '
                    'DIR is created, and is passed into the config as "SIMULATED_SWITCHES_DIR".')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

config = SwitchesConfig()
if args.simulated_switches_dir is not None:
    os.makedirs(args.simulated_switches_dir, exist_ok=True)
    config.set_simulated_switches_dir(args.simulated_switches_dir)

config.parse(args.config, bus=bus)

objects = [
    ('/', SwitchCenter_Server(names=[name for name,_,_ in config.get_switches()]))
]

for name, description, switch in config.get_switches():
    objects.append(('/switches/'+name, Switch_Server(switch=switch)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.SWITCHES,
    objects=objects,
)
