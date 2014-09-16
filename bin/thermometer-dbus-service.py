#!/usr/bin/python3

from heating.thermometer_dummy import DummyThermometer
from heating.thermometer_dbus_object import DBusThermometerObject
import heating.dbus_util as dbus_util

import dbus
import dbus.bus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import logging
from argparse import ArgumentParser
import sys

# parameters
ADDRESS = BUS_NAME = PARENT_PATH = None

parser = ArgumentParser()

parser.add_argument('--address', type=str, help='DBus daemon address')
parser.add_argument('--bus-name', type=str, help='Bus name (also known as connection name)')
parser.add_argument('--parent-path', type=str, help='Path where thermometer objects appear under')

args = parser.parse_args()

ADDRESS = args.address
BUS_NAME = args.bus_name
PARENT_PATH = args.parent_path

mainloop = DBusGMainLoop(set_as_default=True)

try:
    connection = dbus.bus.BusConnection(ADDRESS, mainloop=mainloop)
except dbus.exceptions.DBusException as e:
    logging.exception('cannot connect to '+ADDRESS)
    sys.exit(1)
    
connection.set_exit_on_disconnect(True)
busname = dbus.service.BusName(BUS_NAME, connection)

DBusThermometerObject(
    connection = connection,
    object_path = PARENT_PATH+'/top',
    thermometer = DummyThermometer(85.6))
DBusThermometerObject(
    connection = connection,
    object_path = PARENT_PATH+'/middle',
    thermometer = DummyThermometer(81.2))
DBusThermometerObject(
    connection = connection,
    object_path = PARENT_PATH+'/bottom',
    thermometer = DummyThermometer(76.9))

GLib.MainLoop().run()
