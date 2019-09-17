from . import names
from . import ifaces
from .thermometer import Thermometer_Client
from .temperature_history import TemperatureHistory_Client
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
        proxy = self.connection.get_client_proxy(
            busname=names.BUS.THERMOMETER_SERVICE,
            path='/thermometers/'+name, 
            iface=names.IFACE.THERMOMETER)
        return Thermometer_Client(proxy=proxy)

    def get_history(self, name):
        proxy = self.connection.get_client_proxy(
            busname=names.BUS.THERMOMETER_SERVICE,
            path='/history/'+name, 
            iface=names.IFACE.TEMPERATURE_HISTORY)
        return TemperatureHistory_Client(proxy=proxy)


@ifaces.THERMOMETER_CENTER.iface
class ThermometerCenter_Server:
    def __init__(self, thermometers):
        self.__thermometers = thermometers

    @ifaces.THERMOMETER_CENTER.all_names
    def all_names(self):
        try:
            return [list(self.__thermometers.keys())]
        except HeatingError as e:
            raise ravel.ErrorReturn(name=names.DATA.ERROR, message=str(e))
