from . import interface_repo
from . import node
from . import error
from . import names
from . import _util
from .circuit import Circuit_Client


class CircuitCenter_Client:
    def __init__(self, bus):
        self.__bus = bus
        self.__iface = _util.get_iface(
            bus=bus,
            busname=names.Bus.CIRCUITS,
            path='/',
            iface=interface_repo.CIRCUITCENTER)

    @error.maperror
    def all_names(self):
        return self.__iface.all_names()

    @error.maperror
    def get_circuit(self, name):
        return Circuit_Client(proxy=_util.get_iface(
            bus=self.__bus, 
            busname=names.Bus.CIRCUITS,
            path='/circuits/'+name, 
            iface=interface_repo.CIRCUIT))

    @error.maperror
    def poll(self, timestamp):
        return self.__iface.poll(timestamp)


@node.Definition(interfaces=interface_repo.get(
    interface_repo.CIRCUITCENTER, 
    interface_repo.POLLABLE))
class CircuitCenter_Server:
    def __init__(self, objects):
        self.__objects = objects

    def all_names(self):
        return [o.get_name() for o in self.__objects]

    def poll(self, timestamp):
        for o in self.__objects:
            o.poll(timestamp)
