#!/usr/bin/python3

from openheating.thermometers_ini import read_file as read_config_file
from openheating.thermometer_history import ThermometerHistory
from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection
from openheating.dbus.thermometer import Thermometer_Server
from openheating.dbus.thermometer_center import ThermometerCenter_Server
from openheating.dbus.thermometer_history import ThermometerHistory_Server

import datetime
import asyncio
import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--configfile', help='Thermometer configuration file')
cmdline.add_dbus_options(parser)
args = parser.parse_args()

thermometers = read_config_file(args.configfile)

loop = asyncio.get_event_loop()

connection = Connection(
    is_session=cmdline.is_session(args),
    busname=names.BUS.THERMOMETER_SERVICE)

objects = {
    '/': ThermometerCenter_Server(thermometers=thermometers),
}
for name, thermometer in thermometers.items():
    decision_history = ThermometerHistory(interval=1, duration=datetime.timedelta(minutes=30))
    hour_history = ThermometerHistory(interval=20, duration=datetime.timedelta(hours=1))
    day_history = ThermometerHistory(interval=60, duration=datetime.timedelta(hours=1))

    objects['/thermometers/'+name] = Thermometer_Server(
        interval=5, 
        thermometer=thermometer,
        histories = (decision_history, hour_history, day_history),
    )
    objects['/history/'+name] = ThermometerHistory_Server(
        decision_history=decision_history,
        hour_history=hour_history,
        day_history=day_history,
    )

loop.run_until_complete(connection.run(objects=objects))
loop.close()
