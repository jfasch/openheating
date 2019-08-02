from . import names
from ..switch import Switch

import ravel


@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.SWITCH)
class DBusSwitch:
    def __init__(self, switch):
        assert isinstance(switch, Switch)
        self.switch = switch

    @ravel.method(
        name = 'get_state',
        in_signature = '',
        out_signature = 'b')
    def get_state(self):
        try:
            return (self.switch.get_state(),)
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))

    @ravel.method(
        name = 'set_state',
        in_signature = 'b',
        out_signature = '')
    def set_state(self, value):
        try:
            self.switch.set_state(value)
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))
