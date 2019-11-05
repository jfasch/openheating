from . import interface_repo
from . import node
from . import names
from .thermometer import Thermometer_Client, TemperatureHistory_Client

from ..base.error import HeatingError


class ThermometerCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = self.__get_object_iface(
            busname=names.Bus.THERMOMETERS,
            path='/',
            iface=interface_repo.THERMOMETERCENTER)

    @node.maperror
    def all_names(self):
        return self.__iface.all_names()

    @node.maperror
    def get_thermometer(self, name):
        return Thermometer_Client(
            proxy=self.__get_object_iface(
                busname=names.Bus.THERMOMETERS,
                path='/thermometers/'+name, 
                iface=interface_repo.THERMOMETER))

    @node.maperror
    def get_history(self, name):
        return TemperatureHistory_Client(
            proxy=self.__get_object_iface(
                busname=names.Bus.THERMOMETERS,
                path='/thermometers/'+name, 
                iface=interface_repo.TEMPERATUREHISTORY))

    def __get_object_iface(self, busname, path, iface):
        return self.__bus.get(busname, path)[iface]
    

@node.Definition(interfaces=interface_repo.get(interface_repo.THERMOMETERCENTER))
class ThermometerCenter_Server:
    def __init__(self, thermometers):
        self.__thermometers = thermometers

    def all_names(self):
        return self.__thermometers.keys()
