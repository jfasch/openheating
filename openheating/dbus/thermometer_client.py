from .rebind import DBusObjectClient

from ..thermometer import Thermometer


class DBusThermometer(Thermometer, DBusObjectClient):
    '''A DBusObjectClient which is-a Thermometer. To be used as a local
    Thermometer, asking its temperature over DBus.
    '''

    def temperature(self):
        return float(self.dbus_call('temperature'))
