from . import dbus_util

import dbus.service

class DBusThermometerObject(dbus.service.Object):
    def __init__(self, connection, object_path, thermometer):
        self.__thermometer = thermometer
        dbus.service.Object.__init__(self, conn=connection, object_path=object_path)

    @dbus.service.method(dbus_interface=dbus_util.DBUS_THERMOMETER_IFACE_STRING, out_signature = 'd')
    def temperature(self):
        return self.__thermometer.temperature()

