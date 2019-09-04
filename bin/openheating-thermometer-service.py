#!/usr/bin/python3

from openheating.thermometers_ini import read_file as read_config_file
from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection
from openheating.dbus.thermometer import Thermometer_Server
from openheating.dbus.thermometer_center import ThermometerCenter_Server

import asyncio
import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--configfile', help='Thermometer configuration file')
cmdline.add_dbus_options(parser)
args = parser.parse_args()

thermometers = read_config_file(args.configfile)

connection = Connection(
    is_session=cmdline.is_session(args),
    busname=names.BUS.THERMOMETER_SERVICE)
connection.register_object(
    path='/', 
    object=ThermometerCenter_Server(thermometers=thermometers))
for name, thermometer in thermometers.items():
    connection.register_object(
        path='/thermometers/'+name,
        object=Thermometer_Server(thermometer=thermometer))

loop = asyncio.get_event_loop()
loop.run_until_complete(connection.run(loop))
