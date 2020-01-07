#!/usr/bin/python3

from openheating.base.history import History
from openheating.base import logutil
from openheating.dbus.pyconf import ThermometersConfig
from openheating.dbus import dbusutil
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
parser.add_argument('--simulated-thermometers-dir', metavar='DIR', 
                    help='Create "thermometer" files in DIR, and read temperatures from there. '
                    'DIR is created, and is passed into the config as "SIMULATED_THERMOMETERS_DIR".')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

config = ThermometersConfig()
if args.simulated_thermometers_dir is not None:
    os.makedirs(args.simulated_thermometers_dir, exist_ok=True)
    config.set_simulated_thermometers_dir(args.simulated_thermometers_dir)

config.parse(args.config, bus=bus)

# update_interval: cmdline overrides config
if args.update_interval is not None:
    config.set_update_interval(args.update_interval)

objects = [
    ('/', ThermometerCenter_Server(thermometers=config.get_thermometers()))
]

for thermometer in config.get_thermometers():
    history = History(duration=datetime.timedelta(days=1))
    objects.append(('/thermometers/'+thermometer.get_name(),
                    Thermometer_Server(
                        update_interval=config.get_update_interval(),
                        thermometer=thermometer,
                        history=history)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.THERMOMETERS,
    objects=objects,
)
