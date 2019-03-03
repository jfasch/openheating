#!/usr/bin/python3

from openheating.thermometers_ini import read as read_thermometers
import openheating.dbus.names as busnames
from openheating.dbus.thermometer import DBusThermometer
from openheating.dbus.thermometer_service import DBusThermometerService

import dbussy
import ravel
import asyncio
import sys


bus_name = busnames.iface_name_pfx + '.ThermometerService'

# ThermometerService is at /
service_object_path = '/'
# Thermometers are in a subdirectory
thermometer_object_path_base = '/thermometers'


thermometers = read_thermometers(sys.stdin)

loop = asyncio.get_event_loop()
bus = ravel.session_bus()
bus.attach_asyncio(loop)
bus.request_name(
    bus_name=bus_name, 
    flags=dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE)

# register service object
bus.register(
    path=service_object_path,
    fallback=True,
    interface=DBusThermometerService(thermometers=thermometers)
  )

# register object for each thermometer
for name, thermometer in thermometers.items():
    bus.register(
        path='/'.join((thermometer_object_path_base, name)),
        fallback=True,
        interface=DBusThermometer(thermometer=thermometer)
    )

loop.run_forever()
