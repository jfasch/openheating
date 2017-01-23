from .client import DBusObjectClient

from ..logic.thermometer import Thermometer


class DBusThermometerClient(Thermometer, DBusObjectClient):
    '''A DBusObjectClient which is-a Thermometer. To be used as a local
    Thermometer, asking its temperature over DBus.
    '''

    def temperature(self):
        return float(self.client_call('temperature'))
