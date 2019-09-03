#!/usr/bin/python3

from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection as DBusConnection
from openheating.dbus.thermometer_center import DBusThermometerCenter_Client


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
thermometer_center = DBusThermometerCenter_Client(connection)

if args.subcommand_name == 'list':
    for name in thermometer_center.all_names():
        if args.read_temperature:
            thermometer = thermometer_center.get_thermometer(name)
            print(name, thermometer.get_temperature())
        else:
            print(name)

elif args.subcommand_name == 'get':
    thermometer = thermometer_center.get_thermometer(args.name)
    print(thermometer.get_temperature())

else:
    top_parser.print_help()
    sys.exit(1)
