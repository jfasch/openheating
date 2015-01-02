from .rebind import DBusObjectClient

from ..thermometer_center import ThermometerCenterBase


class DBusThermometerCenter(ThermometerCenterBase, DBusObjectClient):
    def all_names(self):
        return self.dbus_call('all_names')
    def temperature(self, name):
        return float(self.dbus_call('temperature', name))
