#!/usr/bin/python3

from openheating.thermometers_ini import read as read_thermometers
import openheating.dbus.names as busnames
import openheating.dbus.service as dbus_service
from openheating.dbus.thermometer import DBusThermometer
from openheating.dbus.thermometer_service import DBusThermometerService

import dbussy
import ravel
import asyncio
import sys


busname = busnames.iface_name_pfx + '.ThermometerService'

async def main():
    thermometers = read_thermometers(sys.stdin)
    connection = dbus_service.create_connection(busname=busname)

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
