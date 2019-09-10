from . import names
from .thermometer import Thermometer_Client
from ..error import HeatingError

import ravel


class ThermometerCenter_Client:
    def __init__(self, connection):
        self.proxy = connection.get_client_proxy(
            busname=names.BUS.THERMOMETER_SERVICE,
            path='/', 
            iface=names.IFACE.THERMOMETER_CENTER)
        self.connection = connection

    def all_names(self):
        return self.proxy.all_names()[0]

    def get_thermometer(self, name):
        thermometer_proxy = self.connection.get_client_proxy(
            busname=names.BUS.THERMOMETER_SERVICE,
            path='/thermometers/'+name, 
            iface=names.IFACE.THERMOMETER)
        return Thermometer_Client(proxy=thermometer_proxy)


@ravel.interface(
    ravel.INTERFACE.SERVER,
    name = names.IFACE.THERMOMETER_CENTER)
class ThermometerCenter_Server:
    def __init__(self, thermometers):
        self.__thermometers = thermometers

    @ravel.method(
        name = 'all_names',
        in_signature = '',
        out_signature = 'as')
    def all_names(self):
        try:
            return [list(self.__thermometers.keys())]
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))
