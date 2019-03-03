from . import names

import ravel


iface_name = names.iface_name_pfx + '.ThermometerService'

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = iface_name)
class DBusThermometerService:
    def __init__(self, thermometers):
        self.thermometers = thermometers

    @ravel.method(
        name = 'all_names',
        in_signature = '',
        out_signature = 'as',
    )
    def all_names(self):
        return [list(self.thermometers.keys())]

