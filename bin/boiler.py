#!/usr/bin/python3

import dbus.bus

connection = dbus.bus.BusConnection('tcp:host=heizraum,port=6666')

for n in ('top', 'middle', 'bottom'):
    thermometer = connection.get_object('org.openheating.boiler', '/thermometers/' + n)
    print(thermometer.temperature())
