#!/usr/bin/python3

from openheating.thermometers_ini import read as read_thermometers
import openheating.dbus.names as busnames
import openheating.dbus.service as dbus_service
from openheating.dbus.thermometer import DBusThermometer
from openheating.dbus.thermometer_service import DBusThermometerService

import dbussy
import ravel
import asyncio
import argparse


busname = busnames.iface_name_pfx + '.ThermometerService'

async def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--configfile', default='/etc/openheating/thermometers.conf', help='Configuration file')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--session', action='store_true', help='Connect to the session bus')
    group.add_argument('--system', action='store_true', help='Connect to the system bus')
    args = parser.parse_args()

    thermometers = read_thermometers(open(args.configfile))
    connection = dbus_service.create_connection(busname=busname, session=args.session)

    # register service object
    connection.register(
        path='/',
        fallback=True,
        interface=DBusThermometerService(thermometers=thermometers)
    )

    # register object for each thermometer
    for name, thermometer in thermometers.items():
        connection.register(
            path='/thermometers/'+name,
            fallback=True,
            interface=DBusThermometer(thermometer=thermometer)
        )

    await dbus_service.termination()

asyncio.run(main())
