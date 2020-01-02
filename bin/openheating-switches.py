#!/usr/bin/python3

from openheating.base import logutil
from openheating.dbus import pyconf
from openheating.dbus import dbusutil
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.switch import Switch_Server
from openheating.dbus.switch_center import SwitchCenter_Server

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus switch service')
parser.add_argument('--pyconfigfile', help='Switches configuration file (python)')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

with open(args.pyconfigfile) as f:
    switches = pyconf.read_switches(f, bus)

objects = [
    ('/', SwitchCenter_Server(switches=switches))
]

for switch in switches:
    objects.append(('/switches/'+switch.get_name(), Switch_Server(switch=switch)))

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.SWITCHES,
    objects=objects,
)
