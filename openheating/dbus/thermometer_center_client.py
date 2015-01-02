from .types import exception_dbus_to_local

from ..thermometer_center import ThermometerCenterBase
from .rebind import DBusObjectClient
from ..error import HeatingError, DBusNoConnectionError, DBusNoServiceError

from dbus.exceptions import DBusException


class DBusThermometerCenter(ThermometerCenterBase, DBusObjectClient):
    def all_names(self):
        return self.dbus_call('all_names')
    def temperature(self, name):
        return float(self.dbus_call('temperature', name))
