#!/usr/bin/python3

from openheating.thermometers_ini import read_file as read_config_file
from openheating.dbus import cmdline
import openheating.dbus.names as busnames
from openheating.dbus.connection import Connection as DBusConnection
from openheating.dbus.thermometer import DBusThermometer
from openheating.dbus.thermometer_service import DBusThermometerService

import asyncio
import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--configfile', help='Thermometer configuration file')
cmdline.add_dbus_options(parser)
args = parser.parse_args()

thermometers = read_config_file(args.configfile)

connection = DBusConnection(
    is_session=cmdline.is_session(args),
    busname=busnames.thermometer_service_busname)
connection.register_object(
    path='/', 
    object=DBusThermometerService(thermometers=thermometers))
for name, thermometer in thermometers.items():
    connection.register_object(
        path='/thermometers/'+name,
        object=DBusThermometer(thermometer=thermometer))

loop = asyncio.get_event_loop()
loop.run_until_complete(connection.run(loop))
