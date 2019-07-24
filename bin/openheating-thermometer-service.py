#!/usr/bin/python3

from openheating.thermometers_ini import read_file as read_config_file
import openheating.dbus.names as busnames
import openheating.dbus.service as dbus_service
from openheating.dbus.thermometer import DBusThermometer
from openheating.dbus.thermometer_service import DBusThermometerService

import dbussy
import ravel

import asyncio
import argparse
import logging
import traceback


busname = busnames.iface_name_pfx + '.ThermometerService'

# def exception_handler(loop, context):
#     exc = context.get('exception')
#     tbe = traceback.TracebackException(exc)
#     print(list(tbe.format()))
#     logging.error('Error: '+str(msg))
#     loop.stop()

async def main(loop):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--ini', help='Thermometer configuration file')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')
    args = parser.parse_args()

    thermometers = read_config_file(args.ini)
    connection = dbus_service.create_connection(busname=busname, session=args.session, loop=loop)

    # register service object
    connection.register(
        path='/',
        fallback=True,
        interface=DBusThermometerService(thermometers=thermometers)
    )

    # register object for each thermometer
    for name, thermometer in thermometers.items():
        print(name)
        connection.register(
            path='/thermometers/'+name,
            fallback=True,
            interface=DBusThermometer(thermometer=thermometer)
        )

    await dbus_service.termination(loop)

loop = asyncio.get_event_loop()
# loop.set_exception_handler(exception_handler)
loop.run_until_complete(main(loop))
