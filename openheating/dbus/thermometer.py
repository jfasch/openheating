from . import names

from ..thermometer import Thermometer

import ravel


iface_name = names.iface_name_pfx + '.Thermometer'

@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = iface_name)
class DBusThermometer:
    def __init__(self, thermometer):
        assert isinstance(thermometer, Thermometer)
        self.thermometer = thermometer

    @ravel.method(
        name = 'get_temperature',
        in_signature = '',
        out_signature = 'd',
    )
    def get_temperature(self):
        return (self.thermometer.get_temperature(),)
