from . import interface_repo
from . import node
from . import error
from . import names
from . import _util
from .thermometer import Thermometer_Client, TemperatureHistory_Client


class ThermometerCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = _util.get_iface(
            bus=bus,
            busname=names.Bus.THERMOMETERS,
            path=names.ThermometerPaths.CENTER,
            iface=interface_repo.THERMOMETERCENTER)

    @error.maperror
    def all_names(self):
        return self.__iface.all_names()

    @error.maperror
    def get_thermometer(self, name):
        return Thermometer_Client(proxy=_util.get_iface(
            bus=self.__bus,
            busname=names.Bus.THERMOMETERS,
            path=names.ThermometerPaths.THERMOMETER(name),
            iface=interface_repo.THERMOMETER))

    @error.maperror
    def get_history(self, name):
        return TemperatureHistory_Client(proxy=_util.get_iface(
            bus=self.__bus,
            busname=names.Bus.THERMOMETERS,
            path=names.ThermometerPaths.THERMOMETER(name),
            iface=interface_repo.TEMPERATUREHISTORY))

    @error.maperror
    def force_update(self, timestamp):
        for name in self.all_names():
            self.get_thermometer(name).force_update(timestamp)


@node.Definition(interfaces=interface_repo.get(
    interface_repo.THERMOMETERCENTER,
    interface_repo.POLLABLE))
class ThermometerCenter_Server:
    '''D-Bus object that ... well, sort of ... maintains thermometer
    objects.

    '''
    def __init__(self, objects):
        self.__objects = objects

    def all_names(self):
        ''':returns: list strings; names of maintained thermometers.

        '''
        return [o.get_name() for o in self.__objects]

    def poll(self, timestamp):
        '''Polls all maintained thermometers.

        '''
        for o in self.__objects:
            o.poll(timestamp)
