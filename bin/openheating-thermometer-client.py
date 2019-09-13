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
group = history_parser.add_mutually_exclusive_group(required=True)
group.add_argument('--decision', action='store_true', help='History that heating decision are based upon')
group.add_argument('--hour', action='store_true', help='History an hour in the past')
group.add_argument('--day', action='store_true', help='History a day in the past')

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
    if args.decision:
        samples = history.decision_history()
    elif args.hour:
        samples = history.hour_history()
    elif args.day:
        samples = history.day_history()
    else: assert False, 'argparse must have caught this'
        
    for timestamp, temperature in samples:
        dtstr = str(datetime.datetime.fromtimestamp(timestamp))
        print('{0:<25}{1:<10}'.format(dtstr, temperature))
else:
    top_parser.print_help()
    sys.exit(1)
