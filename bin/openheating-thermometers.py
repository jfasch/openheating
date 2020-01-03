#!/usr/bin/python3

from openheating.base.history import History
from openheating.base import logutil
from openheating.dbus import pyconf
from openheating.dbus import dbusutil
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.thermometer import Thermometer_Server
from openheating.dbus.thermometer_center import ThermometerCenter_Server

from gi.repository import GLib

import datetime
import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--pyconfigfile', help='Thermometer configuration file (python)')
parser.add_argument('--interval', help='Temperature read interval (seconds); default 5; 0 to disable updates', default=5, type=int)
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

with open(args.pyconfigfile) as f:
    thermometers = pyconf.read_thermometers(f, bus)

objects = [
    ('/', ThermometerCenter_Server(thermometers=thermometers))
]

for thermometer in thermometers:
    history = History(duration=datetime.timedelta(days=1))
    objects.append(('/thermometers/'+thermometer.get_name(),
                    Thermometer_Server(
                        update_interval=args.interval,
                        thermometer=thermometer,
                        history=history)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.THERMOMETERS,
    objects=objects,
)
