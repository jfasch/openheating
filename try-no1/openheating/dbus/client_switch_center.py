from .client import DBusObjectClient

from ..logic.switch_center import SwitchCenterBase


class DBusSwitchCenterClient(SwitchCenterBase, DBusObjectClient):
    '''A DBusObjectClient which is-a SwitchCenter. To be used as a
    local one.
    '''

    def all_names(self):
        return self.client_call('all_names')

    def set_state(self, name, value):
        assert type(value) is bool, type(value)
        self.client_call('set_state', name, value)

    def get_state(self, name):
        rv = self.client_call('get_state', name)
        # have to convert from "dbus.Boolean" which slips through
        return rv and True or False
