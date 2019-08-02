#!/usr/bin/python3

from openheating.dbus import cmdline
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
list_parser.add_argument('--print-temperature', action='store_true', help='print temperatures')

get_parser = subparsers.add_parser('get', help='get <name>')
get_parser.add_argument('name', help='thermometer name')

args = top_parser.parse_args()


connection = DBusConnection(is_session=cmdline.is_session(args))

if args.subcommand_name == 'list':
    thermometer_service = connection.get_peer(
        busname='org.openheating.ThermometerService', 
        path='/', 
        iface='org.openheating.ThermometerService')
    for name in thermometer_service.all_names()[0]:
        thermometer = connection.get_peer(
            busname='org.openheating.ThermometerService', 
            path='/thermometers/'+name, 
            iface='org.openheating.Thermometer')
        print(name, thermometer.get_temperature()[0])
elif args.subcommand_name == 'get':
    thermometer = connection.get_peer(
        busname='org.openheating.ThermometerService', 
        path='/thermometers/'+args.name, 
        iface='org.openheating.Thermometer')
    print(thermometer.get_temperature()[0])
else:
    top_parser.print_help()
    sys.exit(1)
