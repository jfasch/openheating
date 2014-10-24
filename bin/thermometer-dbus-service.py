#!/usr/bin/python3

from heating.thermometer_dummy import DummyThermometer
from heating.thermometer_dbus_object import DBusThermometerObject
from heating.thermometer_dbus_config import ThermometerDBusServiceConfigParser
import heating.dbus_util as dbus_util

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import logging
from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument('--config', type=str, help='Configuration file (to be documented)')
args = parser.parse_args()

config = ThermometerDBusServiceConfigParser().parse(open(args.config).read())

mainloop = DBusGMainLoop(set_as_default=True)

try:
    connection = dbus.bus.BusConnection(config.daemon_address(), mainloop=mainloop)
except dbus.exceptions.DBusException as e:
    logging.exception('cannot connect to '+config.daemon_address())
    sys.exit(1)
    
connection.set_exit_on_disconnect(True)
busname = dbus.service.BusName(config.bus_name(), connection)

for t in config.thermometers():
    ctor_params = { 'connection': connection }
    ctor_params.update(t)
    DBusThermometerObject(**ctor_params)

GLib.MainLoop().run()
