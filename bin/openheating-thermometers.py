#!/usr/bin/python3

from openheating.base.history import History
from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.plant.config import ThermometersConfig
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.thermometer import Thermometer_Server
from openheating.dbus.thermometer_center import ThermometerCenter_Server

from gi.repository import GLib

import datetime
import argparse
import os


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--config', help='Configuration file')
parser.add_argument('--update-interval', 
                    help='Temperature read interval (seconds); '
                    'default 5; 0 to disable updates', type=int)
parser.add_argument('--simulation-dir', metavar='DIR', 
                    help='Create "thermometer" files in DIR, and read temperatures from there.')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.THERMOMETERS)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

if args.simulation_dir is not None:
    os.makedirs(args.simulation_dir, exist_ok=True)
config = ThermometersConfig(simulation_dir=args.simulation_dir)
config.parse(args.config, bus=bus)

# update_interval: cmdline overrides config
if args.update_interval is not None:
    config.set_update_interval(args.update_interval)

thermometer_objects = [] # for center to know
path_n_objects = [] # [(path, object)], to publish

for name, description, thermometer in config.get_thermometers():
    history = History(duration=datetime.timedelta(days=1))
    thobj = Thermometer_Server(
        name=name,
        description=description,
        thermometer=thermometer,
        update_interval=config.get_update_interval(),
        history=history)
    thermometer_objects.append(thobj)
    path_n_objects.append(('/thermometers/'+name, thobj))

path_n_objects.append(('/', ThermometerCenter_Server(objects=thermometer_objects)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.THERMOMETERS,
    objects=path_n_objects,
)
