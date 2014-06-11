#!/usr/bin/python3

from heating.thermometer_manager import ThermometerManager
from heating.thermometer_dummy import DummyThermometer
from heating.thermometer import Thermometer

import heating.misc as misc

import dbus
import dbus.service
import dbus.bus
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib, Gio, GObject


configured_thermometers = (('one', DummyThermometer(23.4)), ('two', DummyThermometer(34.5)))


class DBusThermometerServer(dbus.service.Object):
    def __init__(self, bus, object_name, object_path, thermometer):
        self.__thermometer = thermometer
        busname = dbus.service.BusName(object_name, bus)
        dbus.service.Object.__init__(self, bus_name=busname, object_path=object_path)

    @dbus.service.method(dbus_interface=misc.DBUS_THERMOMETER_IFACE_STRING, out_signature = 'd')
    def temperature(self):
        print('fuut')
        return self.__thermometer.temperature()


mainloop = DBusGMainLoop(set_as_default=True)
bus = dbus.bus.BusConnection('tcp:host=localhost,port=6666', mainloop=mainloop)
#bus = dbus.SessionBus()

dbus_thermometer_servers = []
for name, thermometer in configured_thermometers:
    object_name, object_path = misc.dbus_thermometer_object_name_path(name)
    dbus_thermometer_servers.append(
        DBusThermometerServer(
            bus=bus,
            object_name=object_name,
            object_path=object_path,
            thermometer=thermometer))

GLib.MainLoop().run()
