#!/usr/bin/python3

from openheating.dbus import cmdline
from openheating.dbus import names
from openheating.dbus.connection import Connection
from openheating.dbus.thermometer_center import ThermometerCenter_Client

import ravel

import argparse
import sys
import time
import datetime


top_parser = argparse.ArgumentParser(
    description='OpenHeating: client for DBus thermometer service')
top_parser.add_argument('--configfile', help='Thermometer configuration file')
cmdline.add_dbus_options(top_parser)

subparsers = top_parser.add_subparsers(dest='subcommand_name')

list_parser = subparsers.add_parser('list')
list_parser.add_argument('--read-temperature', action='store_true', help='read temperatures')

current_parser = subparsers.add_parser('current', help='current <name>')
current_parser.add_argument('name', help='thermometer name')

history_parser = subparsers.add_parser('history', help='history <name>')
history_parser.add_argument('name', help='thermometer name')

args = top_parser.parse_args()


connection = Connection(is_session=cmdline.is_session(args))
thermometer_center = ThermometerCenter_Client(connection)

if args.subcommand_name == 'list':
    for name in thermometer_center.all_names():
        if args.read_temperature:
            thermometer = thermometer_center.get_thermometer(name)
            print(name, thermometer.get_temperature())
        else:
            print(name)
elif args.subcommand_name == 'current':
    thermometer = thermometer_center.get_thermometer(args.name)
    print(thermometer.get_temperature())
elif args.subcommand_name == 'history':
    history = thermometer_center.get_history(args.name)
    for timestamp, temperature in history.all():
        dtstr = str(datetime.datetime.fromtimestamp(timestamp))
        print('{0:<25}{1:<10}'.format(dtstr, temperature))
else:
    top_parser.print_help()
    sys.exit(1)
