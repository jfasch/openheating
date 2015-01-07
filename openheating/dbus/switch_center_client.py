from .rebind import DBusObjectClient

from ..switch_center import SwitchCenterBase


class DBusThermometerCenter(SwitchCenterBase, DBusObjectClient):
    '''A DBusObjectClient which is-a SwitchCenter. To be used as a
    local one.
    '''

    def all_names(self):
        return self.dbus_call('all_names')

    def set_state(self, name, value):
        # translate the enum to boolean, for easy dbus transport
        if value == self.OPEN:
            bool_value = False
        elif value == self.CLOSED:
            bool_value = True
        else:
            assert False, value
        self.dbus_call('set_state', name, bool_value)

    def get_state(self, name):
        bool_value = self.dbus_call('get_state', name)
        if bool_value:
            return self.CLOSED
        else:
            return self.OPEN
