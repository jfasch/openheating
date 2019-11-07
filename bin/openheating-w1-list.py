#!/usr/bin/python3

from openheating.base import w1
from openheating.base import thermometers_pyconf

import argparse
import sys


parser = argparse.ArgumentParser(description='OpenHeating: discover One-Wire temperature sensors')
parser.add_argument('--pyconfigfile', help='Thermometer configuration file (python)', default=None)
parser.add_argument('--read-temperature', help='Display values of discovered sensors', action='store_true')
which = parser.add_mutually_exclusive_group(required=True)
which.add_argument('--all', action='store_true', help='List all One-Wire thermometers in the system')
which.add_argument('--configured', action='store_true', help='List only One-Wire thermometers that are found in the config')
which.add_argument('--unconfigured', action='store_true', help='List only One-Wire thermometers that are not found in the config')
args = parser.parse_args()

if (args.configured or args.unconfigured) and not args.pyconfigfile:
    print('configuration file required', file=sys.stderr)
    sys.exit(1)

def print_thermometers(thermometers):
    for th in thermometers:
        print('*'*3)
        print('Name:', th.name)
        print('Description:', th.description)
        print('Path:', th.path)
        if args.read_temperature:
            try:
                temp = th.get_temperature()
                stemp = str(temp)
            except w1.W1ReadError:
                stemp = 'ERROR'
            except Exception as e:
                stemp = str(e)
            print('Temperature:', stemp)

configured_thermometers = []
if args.pyconfigfile:
    with open(args.pyconfigfile) as f:
        configured_thermometers = list(thermometers_pyconf.read(f).values())

available_thermometers = list(w1.available_thermometers())

# replace available with configured thermometers if they refer to the
# same physical device. more helpful output this way.
new_available_thermometers = []
for avth in available_thermometers:
    for confth in configured_thermometers:
        if isinstance(confth, w1.W1Thermometer) and confth.path == avth.path:
            new_available_thermometers.append(confth)
            break
    else:
        new_available_thermometers.append(avth)
available_thermometers = new_available_thermometers


if args.all:
    print_thermometers(available_thermometers)
elif args.configured:
    print_thermometers(configured_thermometers)
elif args.unconfigured:
    unconfigured_thermometers = []
    for avth in available_thermometers:
        for confth in configured_thermometers:
            if confth.path == avth.path: break
        else:
            unconfigured_thermometers.append(avth)
    print_thermometers(unconfigured_thermometers)

