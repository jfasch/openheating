#!/usr/bin/python3

from heating.thermometer_manager import ThermometerManager
from heating.thermometer_dummy import DummyThermometer

import dbus
import dbus.service
import dbus.mainloop
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib, Gio, GObject

NAME = 'org.faschingbauer.ThermometerManager'
PATH = '/org/faschingbauer/ThermometerManager'

th_man = ThermometerManager((('one', DummyThermometer(23.4)), ('two', DummyThermometer(34.5))))

class DBusThermometerManager(dbus.service.Object):
    def __init__(self, bus, name, path):
        busname = dbus.service.BusName(name, bus)
        dbus.service.Object.__init__(self, busname, path)

    @dbus.service.method(NAME, in_signature = 's', out_signature = 'd')
    def temperature(self, name):
        return th_man.temperature(name)

mainloop = DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()

DBusThermometerManager(bus, NAME, PATH)

GLib.MainLoop().run()
