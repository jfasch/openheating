#!/usr/bin/python3

from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection as DBusConnection


import argparse
import sys
import ravel


top_parser = argparse.ArgumentParser(
    description='OpenHeating: client for DBus thermometer service')
top_parser.add_argument('--configfile', help='Thermometer configuration file')
cmdline.add_dbus_options(top_parser)

subparsers = top_parser.add_subparsers(dest='subcommand_name')

list_parser = subparsers.add_parser('list')
list_parser.add_argument('--read-temperature', action='store_true', help='read temperatures')

get_parser = subparsers.add_parser('get', help='get <name>')
get_parser.add_argument('name', help='thermometer name')

args = top_parser.parse_args()


connection = DBusConnection(is_session=cmdline.is_session(args))

if args.subcommand_name == 'list':
    thermometer_center = connection.get_peer(
        busname=names.BUS.THERMOMETER_SERVICE,
        path='/', 
        iface=names.IFACE.THERMOMETER_CENTER)
    for name in thermometer_center.all_names()[0]:
        if args.read_temperature:
            thermometer = connection.get_peer(
                busname=names.BUS.THERMOMETER_SERVICE,
                path='/thermometers/'+name, 
                iface=names.IFACE.THERMOMETER)
            print(name, thermometer.get_temperature()[0])
        else:
            print(name)

elif args.subcommand_name == 'get':
    thermometer = connection.get_peer(
        busname=names.BUS.THERMOMETER_SERVICE,
        path='/thermometers/'+args.name, 
        iface=names.IFACE.THERMOMETER)
    print(thermometer.get_temperature()[0])

else:
    top_parser.print_help()
    sys.exit(1)
