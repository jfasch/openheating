#!/usr/bin/python3

from openheating.thermometer_fixed import FixedThermometer

from gi.repository import GLib
import dbus.bus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop


class DBUSThermometer(dbus.service.Object):
    def __init__(self, bus_name, path, thermometer):
        dbus.service.Object.__init__(self, conn=connection, object_path=path)
        self.__thermometer = thermometer

    @dbus.service.method(dbus_interface='org.openheating.Thermometer', out_signature = 'd')
    def get_temperature(self):
        return self.__thermometer.get_temperature()


mainloop = DBusGMainLoop(set_as_default=True)
connection = dbus.bus.BusConnection('unix:path=/home/jfasch/work/openheating/dbus/run/openheating-dbus-daemon.socket', mainloop=mainloop)
bus_name = dbus.service.BusName('org.openheating.ThermometerService', connection)
connection.set_exit_on_disconnect(True)

th = DBUSThermometer(bus_name, '/a/b', FixedThermometer(1.2))

GLib.MainLoop().run()
