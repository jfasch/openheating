#!/usr/bin/python3

from gi.repository import GLib
import pydbus.bus


class DBUSService(object):
    '''
    <node>
        <interface name='b.l.a.h'>
            <method name='do_something'>
                <arg type='s' name='response' direction='out'/>
            </method>
    	</interface>
    </node>
    '''

    def do_something(self):
        return 'done'


loop = GLib.MainLoop()
#bus = pydbus.bus.SessionBus()
connection = pydbus.bus.connect('unix:path=/tmp/my-own-bus.socket')
bus = pydbus.bus.Bus(connection)

bus.publish('b.l.a.h', DBUSService())
loop.run()
