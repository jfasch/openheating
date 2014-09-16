#!/usr/bin/python3

from heating.thermometer_dummy import DummyThermometer
from heating.thermometer_dbus_object import DBusThermometerObject

import heating.dbus_util as dbus_util

import dbus
import dbus.bus
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib

name, path = dbus_util.dbus_thermometer_object_name_path('boiler')

mainloop = DBusGMainLoop(set_as_default=True)
connection = dbus.bus.BusConnection('tcp:host=localhost,port=6666', mainloop=mainloop)
connection.set_exit_on_disconnect(True)

busname = dbus.service.BusName(name, connection)

DBusThermometerObject(
    connection=connection,
    object_path=path+'/top',
    thermometer=DummyThermometer(85.6))
DBusThermometerObject(
    connection=connection,
    object_path=path+'/middle',
    thermometer=DummyThermometer(81.2))
DBusThermometerObject(
    connection=connection,
    object_path=path+'/bottom',
    thermometer=DummyThermometer(76.9))

GLib.MainLoop().run()
