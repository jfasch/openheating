#!/usr/bin/python3

from openheating.core.thermometer_fixed import FixedThermometer

from gi.repository import GLib
import pydbus.bus


class DBUSThermometer(object):
    '''
    <node>
        <interface name='org.openheating.Thermometer'>
            <method name='get_temperature'>
                <arg type='d' name='response' direction='out'/>
            </method>
    	</interface>
    </node>
    '''

    def __init__(self, thermometer):
        self.__thermometer = thermometer

    def get_temperature(self):
        return self.__thermometer.get_temperature()


loop = GLib.MainLoop()
connection = pydbus.bus.connect('unix:path=/var/run/openheating/openheating-dbus-daemon.socket')
bus = pydbus.bus.Bus(connection)

bus.publish('org.openheating.ThermometerService',
            DBUSThermometer(FixedThermometer(10.5)),
#            ('thermometer-a', DBUSThermometer(FixedThermometer(10.5))),
#            ('thermometer-b', DBUSThermometer(FixedThermometer(11.5))),
            )
loop.run()
