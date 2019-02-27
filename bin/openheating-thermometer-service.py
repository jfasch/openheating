#!/usr/bin/python3

from openheating.thermometers_ini import read as read_thermometers
import openheating.dbus.names as busnames

import dbussy
import ravel
import asyncio
import sys


bus_name = busnames.iface_name_pfx + '.ThermometerService'

service_iface_name = bus_name
service_object_path = '/'

thermometer_iface_name = busnames.iface_name_pfx + '.Thermometer'
thermometer_object_path_base = '/thermometers'

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = service_iface_name)
class ThermometerService:
    def __init__(self, thermometers):
        self.thermometers = thermometers

    @ravel.method(
        name = 'all_names',
        in_signature = '',
        out_signature = 'as',
    )
    def all_names(self):
        return [list(self.thermometers.keys())]

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = thermometer_iface_name)
class Thermometer:
    def __init__(self, thermometer):
        self.thermometer = thermometer

    @ravel.method(
        name = 'get_temperature',
        in_signature = '',
        out_signature = 'd',
    )
    def get_temperature(self):
        return (self.thermometer.get_temperature(),)


thermometers = read_thermometers(sys.stdin)

loop = asyncio.get_event_loop()
bus = ravel.session_bus()
bus.attach_asyncio(loop)
bus.request_name(
    bus_name=bus_name, 
    flags=dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE)
bus.register(
    path=service_object_path,
    fallback=True,
    interface=ThermometerService(thermometers=thermometers)
  )

for name, thermometer in thermometers.items():
    bus.register(
        path='/'.join((thermometer_object_path_base, name)),
        fallback=True,
        interface=Thermometer(thermometer=thermometer)
    )

loop.run_forever()
