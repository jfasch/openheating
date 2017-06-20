#!/usr/bin/python3

from openheating.dbus.names import THERMOMETER_IFACE
from openheating.core.thermometer import Thermometer
from openheating.dbus.thermometer import Thermometer as DBusThermometer

from pydbus import SessionBus
from gi.repository import GLib
import time


class MyThermometer(Thermometer):
    def get_temperature(self):
        return 21.0, time.time()

loop = GLib.MainLoop()    
bus = SessionBus()
bus.publish(THERMOMETER_IFACE, ('/a/b', DBusThermometer(MyThermometer())))

loop.run()
