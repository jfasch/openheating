#!/usr/bin/python3

import argparse
import sys
import ravel


top_parser = argparse.ArgumentParser(
    description='OpenHeating: client for DBus switch service')

top_parser.add_argument('--configfile', help='Switch configuration file')

bus_group = top_parser.add_mutually_exclusive_group(required=True)
bus_group.add_argument('--session', action='store_true', help='Connect to the session bus')
bus_group.add_argument('--system', action='store_true', help='Connect to the system bus')

subparsers = top_parser.add_subparsers(dest='subcommand_name')

list_parser = subparsers.add_parser('list')
list_parser.add_argument('--print-state', action='store_true', help='print switch states')

get_parser = subparsers.add_parser('get', help='get <name>')
get_parser.add_argument('name', help='switch name')

set_parser = subparsers.add_parser('set', help='set <name> true|false')
set_parser.add_argument('name', help='switch name')
set_parser.add_argument('value', help='true|false')

args = top_parser.parse_args()


bus = ravel.session_bus()
service = bus['org.openheating.SwitchService']
sw_service_object = service['/']
sw_service_iface = sw_service_object.get_interface('org.openheating.SwitchService')


if args.subcommand_name == 'list':
    for name in sw_service_iface.all_names()[0]:
        sw_object = service['/switches/'+name]
        sw_iface = sw_object.get_interface('org.openheating.Switch')
        print(name, sw_iface.get_state()[0])
elif args.subcommand_name == 'get':
    sw_object = service['/switches/'+args.name]
    sw_iface = sw_object.get_interface('org.openheating.Switch')
    print(sw_iface.get_state()[0])
elif args.subcommand_name == 'set':
    if args.value == 'true':
        value = True
    elif args.value == 'false':
        value = False
    else:
        assert False

    sw_object = service['/switches/'+args.name]
    sw_iface = sw_object.get_interface('org.openheating.Switch')
    sw_iface.set_state(value)
else:
    top_parser.print_help()
    sys.exit(1)
