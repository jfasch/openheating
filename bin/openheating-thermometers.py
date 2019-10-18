#!/usr/bin/python3

from openheating.thermometers_ini import read_file as read_config_file
from openheating.history import History
from openheating import logutil
from openheating.dbus import dbusutil
from openheating.dbus.util import lifecycle
from openheating.dbus.thermometer import Thermometer_Server
from openheating.dbus.thermometer_center import ThermometerCenter_Server

from gi.repository import GLib

import datetime
import argparse
import logging


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--configfile', help='Thermometer configuration file')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)
thermometers = read_config_file(args.configfile)
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
    busname=dbusutil.THERMOMETERS_BUSNAME,
    objects=objects,
)
