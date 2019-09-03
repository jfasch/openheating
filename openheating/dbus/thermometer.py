from . import names
from ..thermometer import Thermometer
from ..error import HeatingError

import ravel


class DBusThermometer_Client(Thermometer):
    def __init__(self, proxy):
        self.proxy = proxy

        self.name = None
        self.description = None

    def get_name(self):
        if self.name is None:
            self.name = self.proxy.get_name()[0]
        return self.name

    def get_description(self):
        if self.description is None:
            self.description = self.proxy.get_description()[0]
        return self.description

    def get_temperature(self):
        return self.proxy.get_temperature()[0]


@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.THERMOMETER)
class DBusThermometer_Server:
    def __init__(self, thermometer):
        assert isinstance(thermometer, Thermometer)
        self.thermometer = thermometer

    @ravel.method(
        name = 'get_name',
        in_signature = '',
        out_signature = 's')
    def get_name(self):
        return (self.thermometer.get_name(),)

    @ravel.method(
        name = 'get_description',
        in_signature = '',
        out_signature = 's')
    def get_description(self):
        return (self.thermometer.description,)

    @ravel.method(
        name = 'get_temperature',
        in_signature = '',
        out_signature = 'd')
    def get_temperature(self):
        try:
            return (self.thermometer.get_temperature(),)
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))
