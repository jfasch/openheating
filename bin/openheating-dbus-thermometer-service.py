#!/usr/bin/python3

from openheating.thermometer_dbus_object import DBusThermometerObject
from openheating.thermometer_dbus_config import ThermometerDBusServiceConfigParser
import openheating.dbus_util as dbus_util

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import logging
from argparse import ArgumentParser
import sys
import os
import time
import signal

parser = ArgumentParser()
parser.add_argument('--config-file', type=str, help='Configuration file (to be documented)', required=True)
parser.add_argument('--pid-file', type=str, help='PID file (to be documented)')
args = parser.parse_args()

config = ThermometerDBusServiceConfigParser().parse(open(args.config_file).read())

child = None

def terminate_handler(signal, frame):
    if child is not None:
        # kill child. the terminate-signal could well arrive *after*
        # the child has exited and *before* it is restarted, so its
        # pid might not be valid - so we have to ignore errors.
        try:
            os.kill(child, signal)
        except OSError: pass
    sys.exit(0)
signal.signal(signal.SIGTERM, terminate_handler)

while True:
    child = os.fork()
    if child > 0:
        # parent. wait for child, restart and backoff
        died, status = os.wait()
        time.sleep(2)
    else:
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
