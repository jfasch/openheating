#!/usr/bin/python3

from openheating.w1 import available_thermometers, W1Thermometer
from openheating.thermometers_ini import read_file

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: discover One-Wire temperature sensors')
parser.add_argument('--configfile', help='Thermometer configuration file', default=None)
parser.add_argument('--read-temperature', help='Display values of discovered sensors', action='store_true')
args = parser.parse_args()

conf = None
if args.configfile:
    conf = read_file(args.configfile)

for w1_th in available_thermometers():
    print(w1_th.path)
    print(' '*4, 'ID:', w1_th.id)
    if args.read_temperature:
        print(' '*4, 'Current temperature:', w1_th.get_temperature())
    if conf:
        for conf_th in conf.values():
            if type(conf_th) is W1Thermometer and conf_th.id == w1_th.id:
                print(' '*4, 'Name:', conf_th.name)
                print(' '*4, 'Description:', conf_th.description)
                break
        else:
            print(' '*4, '(No configuration found)')
