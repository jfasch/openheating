#!/usr/bin/python3

from openheating.base import w1
from openheating.plant.config_thermometers import ThermometersConfig

import argparse
import sys


parser = argparse.ArgumentParser(description='OpenHeating: discover One-Wire temperature sensors')
parser.add_argument('--config', help='Thermometer configuration file', default=None)
parser.add_argument('--read-temperature', help='Display values of discovered sensors', action='store_true')
which = parser.add_mutually_exclusive_group(required=True)
which.add_argument('--available', action='store_true', help='List physically One-Wire thermometers in the system')
which.add_argument('--configured', action='store_true', help='List only One-Wire thermometers that are found in the config')
which.add_argument('--unconfigured', action='store_true', help='List only One-Wire thermometers that are not found in the config')
args = parser.parse_args()

if (args.configured or args.unconfigured) and not args.config:
    print('configuration file required', file=sys.stderr)
    sys.exit(1)


_RED_BLINK = '\033[5;31m'
_NO_COLOR = '\033[0m'
def print_thermometers(thermometers):
    for name, descr, th in thermometers:
        print('*'*3)
        print('Name:', name)
        print('Description:', descr)
        print('Path:', th.path)
        if args.read_temperature:
            try:
                tempstr = str(th.get_temperature())
            except w1.W1ReadError:
                tempstr = _RED_BLINK + 'ERROR' + _NO_COLOR
            except Exception as e:
                tempstr = _RED_BLINK + str(e) + _NO_COLOR
            print('Temperature:', tempstr)

configured_thermometers = []   # [(name, description, thermometer)]
if args.config:
    with open(args.config) as f:
        config = ThermometersConfig()
        config.parse(args.config, bus=None)
        configured_thermometers = config.get_thermometers()

# collect available into same shape as configured_thermometers
available_thermometers = [(th.id, th.id, th) for th in w1.available_thermometers()]

# replace available with configured thermometers if they refer to the
# same physical device. more helpful output this way.
for i, (_,_,avth) in enumerate(available_thermometers):
    for name, descr, confth in configured_thermometers:
        if isinstance(confth, w1.W1Thermometer) and confth.path == avth.path:
            available_thermometers[i] = (name,descr,confth)
            break

if args.available:
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

