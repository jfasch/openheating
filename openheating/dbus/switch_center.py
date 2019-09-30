assert False, 'switches not yet in use; unmaintained'

from . import names

import ravel


@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.SWITCH_CENTER)
class DBusSwitchCenter:
    def __init__(self, switches):
        self.switches = switches

    @ravel.method(
        name = 'all_names',
        in_signature = '',
        out_signature = 'as')
    def all_names(self):
        return (list(self.switches.keys()),)
