#!/usr/bin/python3

from openheating import thermometers_conf
from openheating.history import History
from openheating import logutil
from openheating.dbus import dbusutil
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.thermometer import Thermometer_Server
from openheating.dbus.thermometer_center import ThermometerCenter_Server

from gi.repository import GLib

import datetime
import argparse
import logging
import sys


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
config_group = parser.add_mutually_exclusive_group(required=True)
config_group.add_argument('--configfile', help='Thermometer configuration file (.ini style)')
config_group.add_argument('--pyconfigfile', help='Thermometer configuration file (python)')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

conffile, read = args.configfile and (args.configfile, thermometers_conf.read_ini) or (args.pyconfigfile, thermometers_conf.read_pyconf)
with open(conffile) as f:
    thermometers = read(f)
loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

objects = [
    ('/', ThermometerCenter_Server(thermometers=thermometers))
]

for name, thermometer in thermometers.items():
    history = History(duration=datetime.timedelta(days=1))
    objects.append(('/thermometers/'+name,
                    Thermometer_Server(
                        update_interval=5, 
                        thermometer=thermometer,
                        history=history)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.THERMOMETERS,
    objects=objects,
)
