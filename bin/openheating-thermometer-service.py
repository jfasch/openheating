#!/usr/bin/python3

from openheating.thermometers_ini import read_file as read_config_file
import openheating.dbus.names as busnames
import openheating.dbus.service as dbus_service
from openheating.dbus.thermometer import DBusThermometer
from openheating.dbus.thermometer_service import DBusThermometerService

import asyncio
import argparse


def create_service(loop, thermometers):
    """Create the thermometer service

    Creates a dbus connection, and registers objects on it:

    * Thermometer service object
    * A thermometer object for each thermometer in `thermometers`

    """

    connection = dbus_service.create_connection(
        busname=busnames.thermometer_service_busname,
        is_session=args.session, 
        loop=loop)

    connection.register(
        path='/',
        fallback=True,
        interface=DBusThermometerService(thermometers=thermometers)
    )
    for name, thermometer in thermometers.items():
        connection.register(
            path='/thermometers/'+name,
            fallback=True,
            interface=DBusThermometer(thermometer=thermometer)
        )
    
    return connection

parser = argparse.ArgumentParser(description='OpenHeating: DBus thermometer service')
parser.add_argument('--configfile', help='Thermometer configuration file')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--session', action='store_true', help='Connect to the session bus')
group.add_argument('--system', action='store_true', help='Connect to the system bus')
args = parser.parse_args()

thermometers = read_config_file(args.ini)

loop = asyncio.get_event_loop()
create_service(loop=loop, thermometers=thermometers)
loop.run_until_complete(dbus_service.graceful_termination(loop))
