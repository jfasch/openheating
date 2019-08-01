from . import names

import ravel


iface_name = names.iface_name_pfx + '.SwitchService'

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = iface_name)
class DBusSwitchService:
    def __init__(self, switches):
        self.switches = switches

    @ravel.method(
        name = 'all_names',
        in_signature = '',
        out_signature = 'as',
    )
    def all_names(self):
        return [list(self.switches.keys())]

