#!/usr/bin/python3

from openheating.switches_ini import read_file as read_config_file
from openheating.dbus import cmdline
from openheating.dbus.connection import Connection as DBusConnection
import openheating.dbus.names as busnames
from openheating.dbus.switch import DBusSwitch
from openheating.dbus.switch_service import DBusSwitchService

import asyncio
import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus switch service')
parser.add_argument('--configfile', help='Switch configuration file')
cmdline.add_dbus_options(parser)
args = parser.parse_args()

switches = read_config_file(args.configfile)

connection = DBusConnection(
    is_session=cmdline.is_session(args),
    busname=busnames.switch_service_busname)
connection.register_object(
    path='/', 
    object=DBusSwitchService(switches=switches))
for name, switch in switches.items():
    connection.register_object(
        path='/switches/'+name,
        object=DBusSwitch(switch=switch))

loop = asyncio.get_event_loop()
loop.run_until_complete(connection.run(loop))
