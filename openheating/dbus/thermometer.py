from . import names
from ..thermometer import Thermometer
from ..error import HeatingError

import ravel


@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.THERMOMETER)
class DBusThermometer:
    def __init__(self, thermometer):
        assert isinstance(thermometer, Thermometer)
        self.thermometer = thermometer

    @ravel.method(
        name = 'get_temperature',
        in_signature = '',
        out_signature = 'd')
    def get_temperature(self):
        try:
            return (self.thermometer.get_temperature(),)
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))
