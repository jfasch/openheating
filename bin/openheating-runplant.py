#!/usr/bin/python3

from openheating.base import logutil
from openheating.dbus import dbusutil
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.runner import Runner_Server
from openheating.dbus.config import RunnerConfig
from openheating.plant.plant import Plant

from gi.repository import GLib

import argparse
import shutil


parser = argparse.ArgumentParser(description='OpenHeating: plant runner service')
parser.add_argument('--config', help='Configuration file')
parser.add_argument('--simulation-dir', metavar='DIR', 
                    help='Create switch and thermometer files in DIR/switches and DIR/thermometers, respectively. '
                    'The subdirectory names are passed directly to the switch and thermometer services')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

loop = GLib.MainLoop()
buskind = dbusutil.buskind_from_argparse(args)
bus = dbusutil.bus_from_argparse(args)

config = RunnerConfig()
if args.simulation_dir is not None:
    config.set_simulation_dir(args.simulation_dir)
config.parse(args.config, bus=bus)

objects = [
    ('/', Runner_Server(plant = Plant(services=config.get_services()),
                        find_exe = shutil.which,
                        bus_kind = buskind,
                        common_args = logutil.get_log_config_from_argparse(args)),
    )
]

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.RUNNER,
    objects=objects,
)
