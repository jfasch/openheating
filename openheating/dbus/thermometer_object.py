from .types import exception_local_to_dbus, DBUS_THERMOMETER_IFACE_STRING

from ..thermometer import Thermometer
from ..error import HeatingError

import dbus
import dbus.service


class DBusThermometerObject(dbus.service.Object):
    '''Adapt a Thermometer into a DBus object at object_path'''

    def __init__(self, connection, object_path, thermometer):
        self.__implementation = thermometer
        if connection.get_connection() is None:
            # test-mode
            return
        dbus.service.Object.__init__(self, conn=connection.get_connection(), object_path=object_path)

    def implementation(self):
        return self.__implementation

    @dbus.service.method(dbus_interface=DBUS_THERMOMETER_IFACE_STRING, out_signature = 'd')
    def temperature(self):
        try:
            return self.__implementation.temperature()
        except HeatingError as e:
            raise exception_local_to_dbus(e)
