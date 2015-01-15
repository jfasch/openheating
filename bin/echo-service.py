#!/usr/bin/python3

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject

mainloop = DBusGMainLoop()
connection = dbus.bus.BusConnection('unix:path=/tmp/my-dbus.socket', mainloop=mainloop)
busname = dbus.service.BusName('x.y.z', connection)

class EchoObject(dbus.service.Object):
    def __init__(self, conn, path):
        dbus.service.Object.__init__(self, conn=conn, object_path=path)

    @dbus.service.method(dbus_interface='some.lousy.echo', in_signature = 's', out_signature = 's')
    def echo(self, string):
        return string

o = EchoObject(connection, '/a/b')

GObject.MainLoop().run()

