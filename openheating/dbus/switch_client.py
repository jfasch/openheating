from .rebind import DBusObjectClient

from ..switch import Switch


class DBusSwitch(Switch, DBusObjectClient):
    '''A DBusObjectClient which is-a Switch. To be used as a local
    Switch, implemented via a remote DBUs Switch Object.
    '''

    def set_state(self, value):
        # translate the enum to boolean, for easy dbus transport
        if value == self.OPEN:
            bool_value = False
        elif value == self.CLOSED:
            bool_value = True
        else:
            assert False, value
        self.dbus_call('set_state', bool_value)

    def get_state(self):
        bool_value = self.dbus_call('get_state')
        if bool_value:
            return self.CLOSED
        else:
            return self.OPEN
