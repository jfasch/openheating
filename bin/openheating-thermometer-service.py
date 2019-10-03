#!/usr/bin/python3

from openheating.thermometers_ini import read_file as read_config_file
from openheating.history import History
from openheating import logutil
from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus import dbusutil
from openheating.dbus.thermometer import Thermometer_Server
from openheating.dbus.thermometer_center import ThermometerCenter_Server
from openheating.dbus.temperature_history import TemperatureHistory_Server

from gi.repository import GLib

import datetime
import argparse
import logging


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--configfile', help='Thermometer configuration file')
cmdline.add_dbus_options(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)
thermometers = read_config_file(args.configfile)
loop = GLib.MainLoop()
bus = cmdline.bus(args)

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
    objects.append(('/history/'+name,
                    TemperatureHistory_Server(history=history)))

dbusutil.graceful_termination(loop)

bus.publish(names.BUS.THERMOMETER_SERVICE, *objects)
loop.run()
