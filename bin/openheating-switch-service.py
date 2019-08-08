#!/usr/bin/python3

from openheating.switches_ini import read_file as read_config_file
from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection as DBusConnection
from openheating.dbus.switch import DBusSwitch
from openheating.dbus.switch_center import DBusSwitchCenter

import asyncio
import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus switch service')
parser.add_argument('--configfile', help='Switch configuration file')
cmdline.add_dbus_options(parser)
args = parser.parse_args()

switches = read_config_file(args.configfile)

connection = DBusConnection(
    is_session=cmdline.is_session(args),
    busname=names.BUS.SWITCH_SERVICE)
connection.register_object(
    path='/', 
    object=DBusSwitchCenter(switches=switches))
for name, switch in switches.items():
    connection.register_object(
        path='/switches/'+name,
        object=DBusSwitch(switch=switch))

loop = asyncio.get_event_loop()
loop.run_until_complete(connection.run(loop))
