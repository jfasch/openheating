from .rebind import DBusObjectClient

from ..thermometer import Thermometer


class DBusThermometer(Thermometer, DBusObjectClient):
    def temperature(self):
        return float(self.dbus_call('temperature'))
