#!/usr/bin/python3

from openheating.base import mplutil
from openheating.dbus import dbusutil
from openheating.dbus.thermometer_center import ThermometerCenter_Client

import argparse
import sys
import time
import datetime


top_parser = argparse.ArgumentParser(
    description='OpenHeating: client for DBus thermometer service')
dbusutil.argparse_add_bus(top_parser)

subparsers = top_parser.add_subparsers(dest='subcommand_name')

list_parser = subparsers.add_parser('list')
list_parser.add_argument('--read-temperature', action='store_true', help='read temperatures')

current_parser = subparsers.add_parser('current', help='current <name>')
current_parser.add_argument('name', help='thermometer name')

history_parser = subparsers.add_parser('history', help='history <name>')
history_parser.add_argument('name', help='thermometer name')
history_parser.add_argument('--granularity', type=int, help='(seconds)', required=True)
history_parser.add_argument('--duration', type=int, help='(seconds)', required=True)
history_parser.add_argument('--plot', action='store_true')

args = top_parser.parse_args()


bus = dbusutil.bus_from_argparse(args)
thermometer_center = ThermometerCenter_Client(bus)

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
    samples = history.distill(granularity=args.granularity, duration=args.duration)

    if args.plot:
        mplutil.show_samples(samples)
    else:
        for timestamp, temperature in samples:
            dtstr = str(datetime.datetime.fromtimestamp(timestamp))
            print('{0:<25}{1:<10}'.format(dtstr, temperature))
else:
    top_parser.print_help()
    sys.exit(1)
