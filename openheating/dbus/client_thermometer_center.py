from .client import DBusObjectClient

from ..thermometer_center import ThermometerCenterBase


class DBusThermometerCenterClient(ThermometerCenterBase, DBusObjectClient):
    '''A DBusObjectClient which is-a ThermometerCenter. To be used as a
    local one.
    '''

    def all_names(self):
        return self.client_call('all_names')
    def temperature(self, name):
        return float(self.client_call('temperature', name))
