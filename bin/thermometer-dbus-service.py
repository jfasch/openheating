#!/usr/bin/python3

from heating.thermometer_manager import ThermometerManager
from heating.thermometer_dummy import DummyThermometer
from heating.thermometer import Thermometer

import heating.dbus_util as dbus_util

import dbus
import dbus.service
import dbus.bus
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib


class DBusThermometerServer(dbus.service.Object):
    def __init__(self, connection, object_path, thermometer):
        self.__thermometer = thermometer
        dbus.service.Object.__init__(self, conn=connection, object_path=object_path)

    @dbus.service.method(dbus_interface=dbus_util.DBUS_THERMOMETER_IFACE_STRING, out_signature = 'd')
    def temperature(self):
        print('fuut')
        return self.__thermometer.temperature()


mainloop = DBusGMainLoop(set_as_default=True)
connection = dbus.bus.BusConnection('tcp:host=localhost,port=6666', mainloop=mainloop)
busname = dbus.service.BusName('org.openheating.Thermometer.the-connection-from-boiler', connection)

DBusThermometerServer(
    connection=connection,
    object_path='/org/openheating/Thermometer/boiler/one',
    thermometer=DummyThermometer(23.4))
DBusThermometerServer(
    connection=connection,
    object_path='/org/openheating/Thermometer/boiler/two',
    thermometer=DummyThermometer(34.5))

GLib.MainLoop().run()
