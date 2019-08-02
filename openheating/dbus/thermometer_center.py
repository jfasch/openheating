from . import names
from ..error import HeatingError

import ravel


@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.THERMOMETER_CENTER)
class DBusThermometerCenter:
    def __init__(self, thermometers):
        self.thermometers = thermometers

    @ravel.method(
        name = 'all_names',
        in_signature = '',
        out_signature = 'as')
    def all_names(self):
        try:
            return [list(self.thermometers.keys())]
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))
