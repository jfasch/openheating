#!/usr/bin/python3

from argparse import ArgumentParser
import re
import os.path
import sys
import os

parser = ArgumentParser()
parser.add_argument('--config-file', type=str, help='Configuration file (to be documented)', required=True)
parser.add_argument('--action', type=str, help='Action: "add" or "remove"', required=True)
args = parser.parse_args()

if not args.action in ('add', 'remove'):
    print("Action must be 'add' or 'remove'", file=sys.stderr)
    sys.exit(1)

rex_sensor = re.compile(r'^\s*I2C\s+(\S+)\s+(\S+)\s+(\S+)\s*$')
rex_emptyline = re.compile(r'^\s*$')

sensorsfile = open(args.config_file)
for s in sensorsfile:
    if rex_emptyline.search(s):
        continue
    match = rex_sensor.search(s)
    if match is None:
        print("Nix match", file=sys.stderr)
        sys.exit(1)
    modname, address, adapter = match.group(1), match.group(2), match.group(3)
    if not os.path.exists(adapter):
        print("No such adapter: "+adapter, file=sys.stderr)
        sys.exit(1)

    if args.action == 'add':
        with open(adapter + '/new_device', 'w') as new_device:
            new_device.write('%s %s' % (modname, address))
    else:
        with open(adapter + '/delete_device', 'w') as delete_device:
            delete_device.write(address)
