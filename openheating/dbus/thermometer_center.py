from . import interface_repo
from . import node
from . import error
from . import names
from .thermometer import Thermometer_Client, TemperatureHistory_Client


class ThermometerCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = self.__get_object_iface(
            busname=names.Bus.THERMOMETERS,
            path='/',
            iface=interface_repo.THERMOMETERCENTER)

    @error.maperror
    def all_names(self):
        return self.__iface.all_names()

    @error.maperror
    def get_thermometer(self, name):
        return Thermometer_Client(
            proxy=self.__get_object_iface(
                busname=names.Bus.THERMOMETERS,
                path='/thermometers/'+name, 
                iface=interface_repo.THERMOMETER))

    @error.maperror
    def get_history(self, name):
        return TemperatureHistory_Client(
            proxy=self.__get_object_iface(
                busname=names.Bus.THERMOMETERS,
                path='/thermometers/'+name, 
                iface=interface_repo.TEMPERATUREHISTORY))

    @error.maperror
    def force_update(self, timestamp):
        for name in self.all_names():
            self.get_thermometer(name).force_update(timestamp)

    def __get_object_iface(self, busname, path, iface):
        return self.__bus.get(busname, path)[iface]


@node.Definition(interfaces=interface_repo.get(interface_repo.THERMOMETERCENTER))
class ThermometerCenter_Server:
    def __init__(self, objects):
        self.__objects = objects

    def all_names(self):
        return [o.get_name() for o in self.__objects]
