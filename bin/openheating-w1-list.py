#!/usr/bin/python3

from openheating.w1 import available_thermometers
from openheating.thermometers_ini import read as read_ini

import argparse


parser = argparse.ArgumentParser(description='Discover One-Wire temperature sensors')
parser.add_argument('--ini', help='Thermometer configuration file', default=None)
parser.add_argument('--read-temperature', help='Display values of discovered sensors', action='store_true')
args = parser.parse_args()

ini = None
if args.ini:
    ini = read_ini(args.ini)

for th in available_thermometers():
    print(th.path)
    print(' '*4, 'ID:', th.id)
    if args.read_temperature:
        print(' '*4, 'Current temperature:', th.get_temperature())
    if ini:
        for ini_th in ini.values():
            if ini_th.type == th.type and ini_th.id == th.id:
                print(' '*4, 'Description:', ini_th.description)
                break
        else:
            print(' '*4, '(No configuration found)')
