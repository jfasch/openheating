from .client import DBusObjectClient

from ..switch import Switch


class DBusSwitchClient(Switch, DBusObjectClient):
    '''A DBusObjectClient which is-a Switch. To be used as a local
    Switch, implemented via a remote DBUs Switch Object.
    '''

    def set_state(self, value):
        assert type(value) is bool
        self.dbus_call('set_state', value)

    def get_state(self):
        return self.dbus_call('get_state')
