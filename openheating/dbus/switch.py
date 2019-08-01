from . import names

from ..switch import Switch

import ravel


iface_name = names.iface_name_pfx + '.Switch'

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = iface_name)
class DBusSwitch:
    def __init__(self, switch):
        assert isinstance(switch, Switch)
        self.switch = switch

    @ravel.method(
        name = 'get_state',
        in_signature = '',
        out_signature = 'b',
    )
    def get_state(self):
        return (self.switch.get_state(),)

    @ravel.method(
        name = 'set_state',
        in_signature = 'b',
        out_signature = '',
    )
    def set_state(self, value):
        self.switch.set_state(value)
