#!/usr/bin/python3

import heating.dbus_util as dbus_util

import dbus.bus

name, path = dbus_util.dbus_thermometer_object_name_path('boiler')

connection = dbus.bus.BusConnection('tcp:host=localhost,port=6666')
thermometer = connection.get_object(name, path + '/top')
print(thermometer.temperature())
