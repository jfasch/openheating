#!/usr/bin/python3

from openheating.w1 import available_thermometers, W1Thermometer
from openheating.thermometers_ini import read_file

import argparse
import sys


parser = argparse.ArgumentParser(description='OpenHeating: discover One-Wire temperature sensors')
parser.add_argument('--configfile', help='Thermometer configuration file', default=None)
parser.add_argument('--read-temperature', help='Display values of discovered sensors', action='store_true')
parser.add_argument('--unconfigured-only', help='Display only sensors not found in the config', action='store_true')
args = parser.parse_args()

if args.unconfigured_only and not args.configfile:
    print('--unconfigured-only requires --configfile', file=sys.stderr)
    sys.exit(1)

conf = {}
if args.configfile:
    conf = read_file(args.configfile)

def print_sensor(path, id, name, description, temperature):
    print(path)
    print(' '*4, 'ID:', id)
    if temperature is not None:
        print(' '*4, 'Current temperature:', temperature)
    if name is not None:
        print(' '*4, 'Name:', name)
    if description is not None:
        print(' '*4, 'Description:', description)

for w1_th in available_thermometers():
    path = w1_th.path
    id = w1_th.id
    name = description = None
    configured = False
    for conf_th in conf.values():
        if type(conf_th) is W1Thermometer and conf_th.id == id:
            name = conf_th.name
            description = conf_th.description
            configured = True
            break

    if not args.unconfigured_only or args.unconfigured_only and not configured:
        print_sensor(path=path, id=id, name=name, description=description,
                     temperature=args.read_temperature and w1_th.get_temperature() or None)
