#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.plant.config import PlantConfig
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.main import Main_Server

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus circuit service')
parser.add_argument('--config', help='Main/plant configuration file')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.MAIN)

loop = GLib.MainLoop()
bus = dbusutil.bus_from_argparse(args)

config = PlantConfig()
config.parse(args.config, bus=bus)

main_object = Main_Server(bus=bus, services=config.get_services())

lifecycle.run_server(
    loop=loop,
    bus=bus,
    busname=names.Bus.MAIN,
    objects=[('/', main_object)],
)
