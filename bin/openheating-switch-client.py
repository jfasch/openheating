#!/usr/bin/python3

from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection as DBusConnection

import argparse
import sys
import ravel


top_parser = argparse.ArgumentParser(
    description='OpenHeating: client for DBus switch service')
top_parser.add_argument('--configfile', help='Switch configuration file')
cmdline.add_dbus_options(top_parser)

subparsers = top_parser.add_subparsers(dest='subcommand_name')

list_parser = subparsers.add_parser('list')
list_parser.add_argument('--print-state', action='store_true', help='print switch states')

get_parser = subparsers.add_parser('get', help='get <name>')
get_parser.add_argument('name', help='switch name')

set_parser = subparsers.add_parser('set', help='set <name> true|false')
set_parser.add_argument('name', help='switch name')
set_parser.add_argument('value', help='true|false')

args = top_parser.parse_args()


connection = DBusConnection(is_session=cmdline.is_session(args))

if args.subcommand_name == 'list':
    switch_center = connection.get_peer(
        busname=names.BUS.SWITCH_SERVICE, 
        path='/', 
        iface=names.IFACE.SWITCH_CENTER)
    for name in switch_center.all_names()[0]:
        switch = connection.get_peer(
            busname=names.BUS.SWITCH_SERVICE, 
            path='/switches/'+name, 
            iface=names.IFACE.SWITCH)
        print(name, switch.get_state()[0])

elif args.subcommand_name == 'get':
    switch = connection.get_peer(
        busname=names.BUS.SWITCH_SERVICE, 
        path='/switches/'+args.name, 
        iface=names.IFACE.SWITCH)
    print(switch.get_state()[0])

elif args.subcommand_name == 'set':
    if args.value == 'true':
        value = True
    elif args.value == 'false':
        value = False
    else:
        assert False

    switch = connection.get_peer(
        busname=names.BUS.SWITCH_SERVICE, 
        path='/switches/'+args.name, 
        iface=names.IFACE.SWITCH)
    switch.set_state(value)

else:
    top_parser.print_help()
    sys.exit(1)
